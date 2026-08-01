'use client'

import { useEffect, useState } from "react"
import {
  Users,
  MessageSquare,
  CalendarCheck,
  TrendingUp
} from "lucide-react"

interface AnalyticsData {
  total_leads: number
  active_conversations: number
  total_bookings: number
  conversion_rate: number
}

export default function AnalyticsPage() {

  const [data, setData] = useState<AnalyticsData>({
    total_leads: 0,
    active_conversations: 0,
    total_bookings: 0,
    conversion_rate: 0
  })

  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("http://localhost:8000/api/analytics/summary")
      .then(res => res.json())
      .then(result => {
        setData(result)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])


  const cards = [
    {
      title: "Total Leads",
      value: data.total_leads,
      icon: Users
    },
    {
      title: "Active Conversations",
      value: data.active_conversations,
      icon: MessageSquare
    },
    {
      title: "Bookings",
      value: data.total_bookings,
      icon: CalendarCheck
    },
    {
      title: "Conversion Rate",
      value: `${data.conversion_rate}%`,
      icon: TrendingUp
    }
  ]


  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <p className="text-white text-xl">
          Loading analytics...
        </p>
      </div>
    )
  }


  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 to-slate-900 p-8">

      <h1 className="text-3xl font-bold text-white mb-8">
        Analytics Dashboard
      </h1>


      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        {cards.map((card,index)=>{

          const Icon = card.icon

          return (
            <div
              key={index}
              className="
              bg-slate-800/60
              border
              border-pink-500/20
              rounded-2xl
              p-6
              backdrop-blur
              hover:border-pink-400
              transition
              "
            >

              <div className="flex justify-between items-center">

                <div>
                  <p className="text-slate-400 text-sm">
                    {card.title}
                  </p>

                  <h2 className="text-4xl font-bold text-white mt-3">
                    {card.value}
                  </h2>
                </div>


                <div className="
                bg-pink-500/20
                p-4
                rounded-xl
                ">

                  <Icon
                    className="text-pink-400"
                    size={28}
                  />

                </div>

              </div>

            </div>
          )

        })}

      </div>


      <div className="
      mt-8
      bg-slate-800/60
      border
      border-pink-500/20
      rounded-2xl
      p-6
      ">

        <h2 className="text-xl text-white font-semibold mb-4">
          CRM Performance
        </h2>


        <div className="text-slate-300 space-y-3">

          <p>
            Leads generated:
            <span className="text-pink-400 ml-2">
              {data.total_leads}
            </span>
          </p>


          <p>
            Successful bookings:
            <span className="text-pink-400 ml-2">
              {data.total_bookings}
            </span>
          </p>


          <p>
            Customer conversion:
            <span className="text-pink-400 ml-2">
              {data.conversion_rate}%
            </span>
          </p>


        </div>

      </div>


    </div>
  )
}