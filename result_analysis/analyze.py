import json
import pandas as pd
import numpy as np
import scipy.stats as stats

# Helper
def fmt_pct(x):
    return round(100 * x, 1)


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


# Load data

SUBMISSIONS_PATH = "submissions.json"
POSTINGS_PATH = "postings.json"
SURVEY_PATH = "post_task_survey_results.csv"

with open(SUBMISSIONS_PATH) as f:
    subs = json.load(f)
subs_df = pd.DataFrame(subs)
print(f"Loaded {len(subs_df)} trial-level submissions.")

with open(POSTINGS_PATH) as f:
    postings = json.load(f)
postings_df = pd.DataFrame(postings)
print(f"Loaded {len(postings_df)} postings.")

survey_df = pd.read_csv(SURVEY_PATH)
print(f"Loaded {len(survey_df)} post-task survey responses.")

# Join ground truth and compute correctness

print_section("Preparing trial-level data")

fraud_map = {p["id"]: p["fraudulent"] for p in postings}
subs_df["true_fraudulent"] = subs_df["posting_id"].map(fraud_map)
subs_df["true_label"] = subs_df["true_fraudulent"].map({0: "real", 1: "fake"})
subs_df["correct"] = subs_df["worker_label"] == subs_df["true_label"]

print("First few rows with ground truth:")
print(subs_df.head())

# Overall condition-level metrics

print_section("Overall performance by condition")

summary_overall = subs_df.groupby("condition").agg(
    trials=("correct", "size"),
    accuracy=("correct", "mean"),
    mean_confidence=("worker_confidence", "mean"),
    mean_time_ms=("time_on_trial_ms", "mean"),
    median_time_ms=("time_on_trial_ms", "median"),
)
print(summary_overall)

acc_base = fmt_pct(summary_overall.loc["baseline", "accuracy"])
acc_ai = fmt_pct(summary_overall.loc["ai", "accuracy"])
time_base_s = summary_overall.loc["baseline", "mean_time_ms"] / 1000
time_ai_s = summary_overall.loc["ai", "mean_time_ms"] / 1000
conf_base = summary_overall.loc["baseline", "mean_confidence"]
conf_ai = summary_overall.loc["ai", "mean_confidence"]

print(f"\nBaseline accuracy: {acc_base}%")
print(f"AI-assisted accuracy: {acc_ai}%")
print(f"Baseline mean time per trial: {time_base_s:.2f}s")
print(f"AI-assisted mean time per trial: {time_ai_s:.2f}s")
print(f"Baseline mean confidence: {conf_base:.2f}")
print(f"AI-assisted mean confidence: {conf_ai:.2f}")

# Per-participant metrics and paired t-tests

print_section("Per-participant metrics and paired t-tests")

per_participant = (
    subs_df.groupby(["worker_id", "condition"])
    .agg(
        accuracy=("correct", "mean"),
        mean_confidence=("worker_confidence", "mean"),
        mean_time_ms=("time_on_trial_ms", "mean"),
    )
    .reset_index()
)

print("Per-participant summary:")
print(per_participant)

pivot_acc = per_participant.pivot(index="worker_id", columns="condition", values="accuracy")
pivot_conf = per_participant.pivot(index="worker_id", columns="condition", values="mean_confidence")
pivot_time = per_participant.pivot(index="worker_id", columns="condition", values="mean_time_ms")


def paired_stats(pivot, label):
    diffs = pivot["ai"] - pivot["baseline"]
    n = len(diffs)
    mean_diff = float(diffs.mean())
    sd_diff = float(diffs.std(ddof=1))
    t_stat, p_val = stats.ttest_rel(pivot["ai"], pivot["baseline"])
    print(f"\nPaired t-test for {label} (ai - baseline):")
    print(f"  n = {n}")
    print(f"  mean diff = {mean_diff:.4f}")
    print(f"  sd diff = {sd_diff:.4f}")
    print(f"  t({n-1}) = {t_stat:.3f}, p = {p_val:.4f}")


paired_stats(pivot_acc, "accuracy")
paired_stats(pivot_conf, "mean confidence")
paired_stats(pivot_time, "mean time (ms)")

# AI-only performance and agreement with AI

print_section("AI model performance and human-AI agreement")

ai_trials = subs_df[subs_df["condition"] == "ai"].copy()
ai_trials["ai_label"] = ai_trials["ai_prediction"].map({0.0: "real", 1.0: "fake"})
ai_trials["ai_correct"] = ai_trials["ai_label"] == ai_trials["true_label"]
ai_trials["agree_with_ai"] = ai_trials["worker_label"] == ai_trials["ai_label"]

ai_acc = ai_trials["ai_correct"].mean()
worker_acc_ai_cond = ai_trials["correct"].mean()
agree_rate = ai_trials["agree_with_ai"].mean()

print(f"AI accuracy (AI condition trials): {fmt_pct(ai_acc)}%")
print(f"Worker accuracy in AI condition: {fmt_pct(worker_acc_ai_cond)}%")
print(f"Workers agreed with AI on {fmt_pct(agree_rate)}% of AI trials.")

# Post-task survey: mental demand and helpfulness

print_section("Post-task survey analysis")

# Rename columns to something nicer
survey = survey_df.rename(
    columns={
        survey_df.columns[0]: "has_ai",
        survey_df.columns[1]: "mental_demand",
        survey_df.columns[2]: "ai_helpful_raw",
        survey_df.columns[3]: "ai_helpful_extra",
    }
)

survey["condition"] = survey["has_ai"].map({"Yes": "ai", "No": "baseline"})

md_summary = survey.groupby("condition")["mental_demand"].agg(["mean", "std", "count"])
print("\nMental demand by condition:")
print(md_summary)

baseline_md = survey[survey["condition"] == "baseline"]["mental_demand"].reset_index(drop=True)
ai_md = survey[survey["condition"] == "ai"]["mental_demand"].reset_index(drop=True)

md_t, md_p = stats.ttest_rel(ai_md, baseline_md)
mean_md_diff = float((ai_md - baseline_md).mean())
print(f"\nPaired t-test for mental demand (ai - baseline):")
print(f"  mean diff = {mean_md_diff:.3f}")
print(f"  t(5) = {md_t:.3f}, p = {md_p:.4f}")

# Helpfulness only defined for AI rows
helpful = survey[survey["condition"] == "ai"]["ai_helpful_raw"]
print(f"\nAI helpfulness (AI condition only):")
print(f"  mean = {helpful.mean():.2f}, sd = {helpful.std(ddof=1):.2f}, n = {len(helpful)}")

