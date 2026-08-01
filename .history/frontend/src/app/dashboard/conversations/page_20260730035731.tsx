"use client";

import { MessageSquare, Send, Phone, User } from "lucide-react";
import { useState, useEffect } from "react";


interface Message {
  id: number;
  role: string;
  content: string;
  created_at: string;
}


interface Lead {
  id: number;
  full_name: string;
  phone?: string | null;
  platform: string;
  status: string;
}


interface Conversation {
  id: number;
  platform: string;
  is_ai_active: boolean;
  lead?: Lead | null;
  messages?: Message[];
  created_at: string;
  updated_at?: string;
}



export default function ConversationsPage() {


  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);



  useEffect(() => {

    fetchConversations();

    const interval = setInterval(
      fetchConversations,
      5000
    );


    return () => clearInterval(interval);


  }, []);



  const fetchConversations = async () => {

    try {

      const res = await fetch(
        "http://localhost:8000/api/conversations/"
      );


      if (!res.ok) {
        throw new Error(
          "Failed to fetch conversations"
        );
      }


      const data = await res.json();



      const normalized = data.map(
        (conv: Conversation) => ({
          ...conv,
          messages: conv.messages ?? []
        })
      );



      setConversations(normalized);



      if (
        normalized.length > 0 &&
        selected === null
      ) {

        setSelected(
          normalized[0].id
        );

      }



    } catch (error) {

      console.error(
        "Conversation fetch error:",
        error
      );


    } finally {

      setLoading(false);

    }

  };





  const handleSendMessage = async () => {


    if (
      !message.trim() ||
      !selected
    ) {
      return;
    }



    try {


      const res = await fetch(

        `http://localhost:8000/api/conversations/${selected}/send`,

        {

          method: "POST",

          headers: {

            "Content-Type":
              "application/json"

          },


          body: JSON.stringify({

            content: message

          })

        }

      );



      if(res.ok){

        setMessage("");

        await fetchConversations();

      }



    } catch(error){

      console.error(
        "Send message error:",
        error
      );

    }

  };





  const active =
    conversations.find(
      c => c.id === selected
    );






  if(loading){


    return (

      <div className="space-y-6">

        <h1 className="text-xl font-semibold text-white flex items-center gap-2">

          <MessageSquare className="w-5 h-5 text-accent"/>

          Conversations

        </h1>


        <div className="flex justify-center items-center h-96">

          <p className="text-slate-400">
            Loading...
          </p>

        </div>


      </div>

    );

  }





  return (

    <div className="space-y-6 animate-fade-in">


      <h1 className="text-xl font-semibold text-white flex items-center gap-2">

        <MessageSquare className="w-5 h-5 text-accent"/>

        Conversations

      </h1>





      <div className="grid grid-cols-3 gap-4 h-[600px]">


        <div className="glass-card overflow-y-auto">


          {
          conversations.length === 0 ? (

            <div className="p-5 text-center text-slate-500">

              No conversations yet

            </div>


          ) : (


            conversations.map(conv => (

              <div

                key={conv.id}

                onClick={() =>
                  setSelected(conv.id)
                }


                className={`p-4 border-b cursor-pointer transition-all ${
                  
                  selected === conv.id

                  ? "bg-accent/10"

                  : "hover:bg-white/[0.03]"

                }`}

              >


                <div className="flex items-center gap-3">


                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-accent to-violet-500 flex items-center justify-center text-white font-bold">

                    {
                      conv.lead?.full_name?.[0]
                      ??
                      "?"
                    }


                  </div>



                  <div>


                    <p className="text-white text-sm">

                      {
                        conv.lead?.full_name
                        ??
                        "Unknown"
                      }

                    </p>



                    <p className="text-slate-500 text-xs">


                      {conv.platform}

                      {" • "}

                      {
                        conv.messages?.length
                        ??
                        0
                      }

                      {" messages"}


                    </p>


                  </div>


                </div>



              </div>


            ))

          )

          }


        </div>







        <div className="col-span-2 glass-card flex flex-col">


        {

        active ? (

        <>


        <div className="p-4 border-b flex justify-between">


          <div className="flex gap-3">


            <User className="text-accent"/>


            <div>


              <p className="text-white">

                {
                  active.lead?.full_name
                  ??
                  "Unknown"
                }

              </p>


              <p className="text-slate-500 text-xs">

                {active.platform}

                {" • "}

                {
                  active.lead?.phone
                  ??
                  "-"
                }

              </p>


            </div>


          </div>



          <Phone className="text-accent"/>


        </div>





        <div className="flex-1 overflow-y-auto p-4 space-y-4">


        {

        active.messages?.length === 0 ? (


          <div className="text-center text-slate-500">

            No messages yet

          </div>


        ) : (

          active.messages?.map(msg => (


            <div
            key={msg.id}
            className={`flex ${
              msg.role === "user"
              ?
              "justify-start"
              :
              "justify-end"
            }`}
            >


              <div className="bg-white/[0.08] rounded-lg px-4 py-2">


                <p className="text-white text-sm">

                  {msg.content}

                </p>


              </div>



            </div>


          ))


        )


        }


        </div>





        <div className="p-4 border-t flex gap-2">


          <input

          value={message}

          onChange={
            e =>
            setMessage(e.target.value)
          }

          onKeyDown={
            e =>
            e.key==="Enter"
            &&
            handleSendMessage()
          }


          placeholder="Type message..."

          className="input-dark flex-1"

          />


          <button

          onClick={handleSendMessage}

          className="bg-accent px-4 rounded-xl text-white"

          >

            <Send size={18}/>

          </button>


        </div>



        </>


        ) : (


        <div className="flex items-center justify-center h-full text-slate-400">

          Select conversation

        </div>


        )


        }



        </div>


      </div>



    </div>


  );

}