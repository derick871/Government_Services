import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import AdminConsole from "./pages/AdminConsole";
import TrackService from "./pages/TrackService";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/adminconsole" element={<AdminConsole />} />
        <Route path="/trackservice" element={<TrackService />} />
      </Routes>
    </BrowserRouter>
  );
}
