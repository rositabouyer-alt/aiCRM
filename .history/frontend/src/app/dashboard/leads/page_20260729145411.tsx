'use client'

import { useState, useEffect } from 'react'
import { Plus, Search } from 'lucide-react'

interface Lead {
  id: number
  full_name: string
  phone?: string
  email?: string
  status: string
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetch('http://localhost:8000/api/leads/')
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch leads')
        }
        return res.json()
      })
      .then((data) => {
        setLeads(data)
      })
      .catch((err) => {
        console.error(err)
      })
  }, [])

  const filtered = leads.filter((lead) =>
    (lead.full_name || '')
      .toLowerCase()
      .includes(search.toLowerCase()) ||
    (lead.phone || '').includes(search)
  )

  return (
    <div className="p-8 bg-gradient-to-br from-slate-900 to-slate-800 min-h-screen">

      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">
          Leads
        </h1>

        <button className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus className="w-4 h-4" />
          New Lead
        </button>
      </div>


      <div className="bg-slate-700/50 backdrop-blur rounded-lg p-4 mb-6 border border-pink-500/20">

        <div className="flex items-center gap-2">

          <Search className="w-5 h-5 text-slate-400" />

          <input
            type="text"
            placeholder="Search by name or phone..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-transparent text-white outline-none flex-1"
          />

        </div>

      </div>


      <div className="space-y-4">

        {filtered.map((lead) => (

          <div
            key={lead.id}
            className="bg-slate-700/50 backdrop-blur rounded-lg p-4 border border-pink-500/20 hover:border-pink-400 transition"
          >

            <div className="flex justify-between items-start">

              <div>

                <p className="text-white font-semibold">
                  {lead.full_name}
                </p>

                <p className="text-slate-400 text-sm">
                  {lead.phone || 'No phone'} | {lead.email || 'No email'}
                </p>

              </div>


              <span className="bg-pink-500/20 text-pink-300 px-3 py-1 rounded-full text-sm">
                {lead.status}
              </span>


            </div>

          </div>

        ))}


        {filtered.length === 0 && (

          <div className="text-center text-slate-400 py-10">
            No leads found
          </div>

        )}

      </div>

    </div>
  )
}