import { useState } from "react";

export default function Login() {
    const [email, setEail] = useState("");
    const [password, setPassword] = useState("");

    const loginUser = async (e) => {
        e.preventDefault();
        alert("login successful");

}

return (
    <div className="bg:slate-750, m-10">
        <form
        onSubmit={Login}>
            <h2>
                Citizen Login
            </h2>
            <input type="email" 
            placeholder="Email"
          className="w-full border p-2 mb-4"
          onChange={(e)=>setEmail(e.target.value)}
        />
        <input type="password"
        placeholder="Password"
        className="w-full border p-2 mb-4"
        onChange={(e)=>setPassword(e.target.value)}
        />
        <button type="submit" className="bg:amber-500, text-white, p-2, rounded-md">
            Login
        </button>
        </form>
    </div>

)
}

