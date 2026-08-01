export default function Dashboard() {
    return (
       <div>
        <div className="bg:slate-750, m-10">
            <h1 className="text-white, text-3xl, m-10">Dashboard</h1>
            <p className="text-white, text-xl, m-10">Welcome to the dashboard</p>
        </div>
        <h1 className="text-3xl font-bold">
        Citizen Dashboard
      </h1>

      <div className="grid md:grid-cols-4 gap-6 mt-8">

        <Card title="Submitted" value="10"/>

        <Card title="Approved" value="6"/>

        <Card title="Pending" value="5"/>

        <Card title="Rejected" value="1"/>

        </div>


        </div>
    );
}
function Card({title,value}){

    return(

        <div className="bg-white shadow rounded p-6">

            <h2 className="text-gray-500">{title}</h2>

            <h1 className="text-3xl font-bold">{value}</h1>

        </div>

    )

}