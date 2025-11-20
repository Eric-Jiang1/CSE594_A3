import React from "react";

function asBool(value) {
    return value === 1 || value === "1" || value === true ? "Yes" : "No";
  }
  
  export default function JobCard({ posting }) {
    return (
      <div className="job-card">
        <h2>{posting.title}</h2>
        <p><strong>Location:</strong> {posting.location}</p>
  
        {posting.department && (
          <p><strong>Department:</strong> {posting.department}</p>
        )}
  
        <p><strong>Company:</strong> {posting.company_profile || "Not provided"}</p>
  
        {posting.industry && (
          <p><strong>Industry:</strong> {posting.industry}</p>
        )}
        {posting.function && (
          <p><strong>Function:</strong> {posting.function}</p>
        )}
  
        <h3>Description</h3>
        <p>{posting.description}</p>
  
        <h3>Requirements</h3>
        <p>{posting.requirements}</p>
  
        {posting.benefits && (
          <>
            <h3>Benefits</h3>
            <p>{posting.benefits}</p>
          </>
        )}
  
        <h3>Metadata</h3>
        <p><strong>Employment Type:</strong> {posting.employment_type}</p>
        <p><strong>Required Education:</strong> {posting.required_education}</p>
        <p><strong>Required Experience:</strong> {posting.required_experience}</p>
  
        <p><strong>Telecommuting:</strong> {asBool(posting.telecommuting)}</p>
      </div>
    );
  }
  
  