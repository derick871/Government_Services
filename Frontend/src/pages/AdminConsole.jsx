export default function AdminConsole(){

    return(

        <div className="p-8">

            <h1 className="text-3xl font-bold">
                Admin Console
            </h1>

            <table className="w-full mt-8 border">

                <thead className="bg-blue-700 text-white">

                    <tr>

                        <th className="p-3">Reference</th>

                        <th>Name</th>

                        <th>Status</th>

                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    <tr className="text-center border">

                        <td className="p-3">
                            GST-1001
                        </td>

                        <td>
                            Derrick
                        </td>

                        <td>
                            Pending
                        </td>

                        <td>

                            <button className="bg-green-600 text-white px-3 py-1 rounded">
                                Review
                            </button>

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    )

}