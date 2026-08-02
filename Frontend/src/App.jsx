import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import adminconsole from "./pages/adminconsole";
import TrackService from "./pages/TrackService";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/adminconsole" element={<adminconsole />} />
        <Route path="/trackservice" element={<TrackService />} />
      </Routes>
    </BrowserRouter>
  );
}
