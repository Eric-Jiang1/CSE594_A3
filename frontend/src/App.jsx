import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Task from "./pages/Task";
import Complete from "./pages/Complete";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/task" element={<Task />} />
        <Route path="/complete" element={<Complete />} />
      </Routes>
    </BrowserRouter>
  );
}
