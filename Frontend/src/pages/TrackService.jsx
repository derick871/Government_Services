export default function TrackService() {

  const steps = [
    "Submitted",
    "Under Review",
    "Approved",
    "Rejected"
  ];

  return (

    <div className="p-8">

      <h1 className="text-3xl font-bold">
        Track Application
      </h1>

      <div className="mt-8">

        {steps.map((step,index)=>(

          <div
            key={index}
            className="flex items-center mb-4"
          >

            <div className="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center">

              

            </div>

            <p className="ml-4">{step}</p>

          </div>

        ))}

      </div>

    </div>

  );

}