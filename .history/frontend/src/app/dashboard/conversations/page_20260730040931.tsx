"use client";

import { MessageSquare, Send, Phone, User } from "lucide-react";
import { useEffect, useState } from "react";


interface Message {
  id: number;
  role: string;
  content: string;
  created_at?: string | null;
}


interface Lead {
  id: number;
  full_name?: string | null;
  phone?: string | null;
  platform?: string | null;
  status?: string | null;
}


interface Conversation {
  id: number;
  platform: string;
  status: string;
  is_ai_active: boolean;
  lead?: Lead | null;
  messages: Message[];
  created_at?: string | null;
  updated_at?: string | null;
}



export default function ConversationsPage() {


  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);



  useEffect(() => {

    loadConversations();

    const timer = setInterval(
      loadConversations,
      5000
    );


    return () => clearInterval(timer);

  }, []);



  async function loadConversations(){

    try{

      const res = await fetch(
        "http://localhost:8000/api/conversations/"
      );


      if(!res.ok){
        throw new Error(
          "Failed loading conversations"
        );
      }


      const data = await res.json();


      const fixed = data.map(
        (item: Conversation)=>({

          ...item,

          messages:
            item.messages ?? []

        })
      );


      setConversations(fixed);



      if(
        fixed.length &&
        selected === null
      ){

        setSelected(
          fixed[0].id
        );

      }


    }catch(error){

      console.error(
        error
      );

    }finally{

      setLoading(false);

    }

  }




  async function sendMessage(){


    if(
      !message.trim() ||
      !selected
    ){
      return;
    }



    try{


      const res = await fetch(

        `http://localhost:8000/api/conversations/${selected}/send`,

        {

          method:"POST",

          headers:{
            "Content-Type":
            "application/json"
          },


          body:JSON.stringify({

            content:message

          })

        }

      );



      if(res.ok){

        setMessage("");

        await loadConversations();

      }


    }catch(error){

      console.error(
        error
      );

    }

  }




  const activeConversation =
    conversations.find(
      item =>
      item.id === selected
    );





  if(loading){

    return (

      <div className="flex items-center justify-center h-96 text-slate-400">

        Loading...

      </div>

    );

  }





  return (

    <div className="space-y-6">


      <h1 className="text-xl font-semibold text-white flex gap-2 items-center">

        <MessageSquare className="text-accent"/>

        Conversations

      </h1>





      <div className="grid grid-cols-3 gap-4 h-[600px]">





        <div className="glass-card overflow-y-auto">


          {
            conversations.length === 0 ?


            (

              <div className="p-5 text-center text-slate-500">

                No conversations

              </div>

            )


            :

            (

            conversations.map(conv=>(


              <div

                key={conv.id}

                onClick={()=>
                  setSelected(conv.id)
                }


                className={`
                p-4 cursor-pointer border-b
                ${
                  selected === conv.id
                  ?
                  "bg-accent/10"
                  :
                  "hover:bg-white/5"
                }
                `}

              >


                <div className="flex gap-3 items-center">


                  <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center text-white">

                    {
                      conv.lead?.full_name?.charAt(0)
                      ||
                      "?"
                    }

                  </div>



                  <div>


                    <p className="text-white text-sm">

                      {
                        conv.lead?.full_name
                        ||
                        "Unknown"
                      }

                    </p>



                    <p className="text-xs text-slate-500">

                      {conv.platform}

                      {" • "}

                      {conv.messages.length}

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

          activeConversation ?


          (

          <>


          <div className="p-4 border-b flex justify-between">


            <div className="flex gap-3 items-center">

              <User className="text-accent"/>


              <div>


                <p className="text-white">

                  {
                    activeConversation.lead?.full_name
                    ||
                    "Unknown"
                  }

                </p>


                <p className="text-xs text-slate-500">

                  {
                    activeConversation.lead?.phone
                    ||
                    "-"
                  }

                </p>


              </div>


            </div>



            <Phone className="text-accent"/>


          </div>







          <div className="flex-1 overflow-y-auto p-4 space-y-3">


          {

          activeConversation.messages.length === 0 ?


          (

            <p className="text-slate-500 text-center">

              No messages

            </p>

          )


          :

          activeConversation.messages.map(msg=>(


            <div

              key={msg.id}

              className={`
              flex
              ${
                msg.role==="user"
                ?
                "justify-start"
                :
                "justify-end"
              }
              `}

            >


              <div className="bg-white/10 rounded-xl px-4 py-2 max-w-md">


                <p className="text-white text-sm">

                  {msg.content}

                </p>


              </div>


            </div>


          ))

          }


          </div>







          <div className="p-4 border-t flex gap-2">


            <input

              value={message}

              onChange={
                e=>
                setMessage(e.target.value)
              }


              onKeyDown={
                e=>
                e.key==="Enter" &&
                sendMessage()
              }


              className="input-dark flex-1"

              placeholder="Write message..."

            />



            <button

              onClick={sendMessage}

              className="bg-accent px-4 rounded-xl text-white"

            >

              <Send size={18}/>

            </button>


          </div>


          </>


          )


          :


          (

          <div className="flex items-center justify-center h-full text-slate-500">

            Select conversation

          </div>

          )


        }


        </div>



      </div>



    </div>

  );


}