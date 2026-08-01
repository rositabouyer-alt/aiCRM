"use client";

import { useEffect, useState } from "react";
import {
  CalendarCheck,
  Plus,
  Clock,
  User,
  MapPin
} from "lucide-react";


interface Booking {
  id: number;
  title: string;
  scheduled_at: string;
  duration_minutes: number;
  location?: string;
  status: string;
  lead?: {
    full_name: string;
  };
}


export default function BookingsPage() {


  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);



  useEffect(() => {

    fetch(
      "http://localhost:8000/api/bookings/"
    )
      .then(res => res.json())
      .then(data => {

        setBookings(data);
        setLoading(false);

      })
      .catch(err => {

        console.error(err);
        setLoading(false);

      });


  }, []);




  if (loading) {

    return (
      <div className="text-white p-8">
        Loading bookings...
      </div>
    );

  }




  return (

    <div className="space-y-6 animate-fade-in">


      <div className="flex items-center justify-between">

        <h1 className="text-xl font-semibold text-white flex items-center gap-2">

          <CalendarCheck className="w-5 h-5 text-accent"/>

          Bookings

        </h1>


        <button className="btn-primary">

          <Plus className="w-4 h-4"/>

          New Booking

        </button>


      </div>





      <div className="grid grid-cols-1 gap-4">


        {
          bookings.map((booking)=>(


            <div
              key={booking.id}
              className="glass-card p-6"
            >


              <div className="flex justify-between mb-4">


                <div>

                  <h3 className="text-white font-semibold">

                    {booking.lead?.full_name || "Unknown Customer"}

                  </h3>


                  <p className="text-slate-400 text-sm">

                    {booking.title}

                  </p>


                </div>



                <span
                  className={`
                  text-xs px-3 py-1 rounded-full
                  ${
                    booking.status === "confirmed"
                    ?
                    "bg-emerald-500/15 text-emerald-400"
                    :
                    "bg-yellow-500/15 text-yellow-400"
                  }
                  `}
                >

                  {booking.status}

                </span>



              </div>





              <div className="grid grid-cols-3 gap-4">



                <div className="flex gap-2">

                  <Clock className="w-4 h-4 text-accent"/>

                  <div>

                    <p className="text-slate-500 text-xs">
                      Time
                    </p>

                    <p className="text-white text-sm">

                      {
                        new Date(
                          booking.scheduled_at
                        ).toLocaleString()
                      }

                    </p>


                  </div>

                </div>





                <div className="flex gap-2">


                  <MapPin className="w-4 h-4 text-accent"/>


                  <div>

                    <p className="text-slate-500 text-xs">
                      Duration
                    </p>


                    <p className="text-white text-sm">

                      {booking.duration_minutes} min

                    </p>


                  </div>


                </div>





                <div className="flex gap-2">

                  <User className="w-4 h-4 text-accent"/>


                  <div>

                    <p className="text-slate-500 text-xs">
                      Customer
                    </p>


                    <p className="text-white text-sm">

                      {booking.lead?.full_name}

                    </p>


                  </div>


                </div>


              </div>





              <div className="flex gap-2 mt-4 pt-4 border-t border-pink-500/[0.06]">


                <button className="btn-primary text-xs">

                  Confirm

                </button>



                <button className="btn-ghost text-xs">

                  Reschedule

                </button>



                <button className="btn-ghost text-xs">

                  Cancel

                </button>


              </div>




            </div>


          ))
        }



      </div>


    </div>

  );

}