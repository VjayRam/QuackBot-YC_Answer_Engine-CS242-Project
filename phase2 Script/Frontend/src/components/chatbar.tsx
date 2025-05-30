import React, { useState, useEffect, useRef } from "react";
import tenorGif from "../assets/tenor.gif"; // Adjust path accordingly
import axios from "axios";

// Adjust path accordingly
interface ChatbarProps {
    company?: string | null;
    setResults: React.Dispatch<React.SetStateAction<any[]>>;
}

interface Message {
    sender: "user" | "bot";
    text: string;
}

const Chatbar: React.FC<ChatbarProps> = ({ company, setResults }) => {
    const [currentSession, setCurrentSession] = useState<string>("General");
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>("");
    const [k, setK] = useState<number>(5); // Default K value to 5
    const chatContainerRef = useRef<HTMLDivElement>(null);
    const [phase, setPhase] = useState<string>("phase1");

    useEffect(() => {
        if (company) {
            setCurrentSession(company);
        } else {
            setCurrentSession("General");
        }
        setMessages([]); // Clear chat on session switch
    }, [company]);

    useEffect(() => {
        // Auto-scroll to the latest message
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    const handleGeneralButton = () => {
        setCurrentSession("General");
        setMessages([]);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            handleSendMessage();
        }
    };

    const getresponse = async (currentSession: string, userMessage: string, k: number) => {
        try {
            const response = await axios.get(
                `http://127.0.0.1:8000/response/${phase}/${currentSession}/${userMessage}/${k}`
            );
            console.log(response["data"]);
            return [response["data"][0], response["data"][1]];
        } catch (error) {
            return `Error Fetching chat: ${error}`;
        }
    };

    const handleSendMessage = async () => {
        if (input.trim() === "") return;

        // User message
        const userMessage: Message = { sender: "user", text: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");

        try {
            const [botReply, indexdata] = await getresponse(currentSession, input, k);

            // Update the index data in context
            const botMessage: Message = {
                sender: "bot",
                text: botReply,
            };
            setMessages((prev) => [...prev, botMessage]);
            setResults(indexdata);
            console.log(indexdata);
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    useEffect(() => {
        const firstMessage = `Quack! How can I help you with ${currentSession}.`;
        const botMessage: Message = { sender: "bot", text: firstMessage };
        setMessages([botMessage]);
    }, [currentSession]);

    return (
        <div className="flex flex-col h-screen w-1/2 border sticky top-0 ">
            {/* Background GIF */}
            {/* <div className="absolute inset-0 z-0 overflow-hidden flex justify-center items-center">
                <img
                    src={tenorGif}
                    alt="Chat Background GIF"
                    className="w-full h-full object-cover opacity-30"
                />
            </div> */}
            {/* Chat Content (Overlay on GIF) */}
            <div className="relative z-10 flex flex-col h-full">
                {/* Chat Header (Fixed) */}
                <div className="p-4 flex justify-between items-center ">
                    <h1 className="text-xl font-bold bg-gray-400 text-white border-2 rounded-full px-4 py-2">{currentSession}</h1>

                    <div className="flex gap-4 border-black">
                        <button
                            className={`p-2 text-xl font-bold ${phase === "phase1" ? "text-black bg-inherit border-2 rounded-2xl" : ""}`}
                            onClick={() => setPhase("phase1")}
                        >
                            PyElastic
                        </button>
                        <button
                            className={`p-2 text-xl font-bold ${phase === "phase2" ? "text-black bg-inherit border-2 rounded-2xl" : ""}`}
                            onClick={() => setPhase("phase2")}
                        >
                            BERT
                        </button>
                    </div>

                    <button
                        className="text-xl font-bold bg-gray-400 bg-opacity-50 text-white border-2 border-white rounded-full px-4 py-2 backdrop-filter backdrop-blur-lg"
                        onClick={handleGeneralButton}
                    >
                        Reset
                    </button>
                </div>

                {/* Chat Messages (Scrollable) */}
                <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`p-2 rounded-lg w-fit max-w-[70%] transition-all duration-500 ${msg.sender === "user" ? "bg-gradient-to-r from-gray-300 to-gray-500 text-black text-black ml-auto" : "bg-gradient-to-l from-gray-300 to-gray-500 text-black text-black"}`}
                        >
                            {msg.text}
                        </div>
                    ))}
                </div>

                {/* Chat Input (Fixed at Bottom) */}
                <div className="p-4 sticky bottom-0">
                    <div className="flex gap-2">
                        {/* K Input Field */}
                        <div className="flex items-center">
                            <label htmlFor="k-input" className="mr-2 text-lg">K-Results:</label>
                            <input
                                id="k-input"
                                type="number"
                                value={k}
                                onChange={(e) => {
                                    const newK = Math.max(1, Math.min(99, Number(e.target.value))); // Restrict to range [1, 99]
                                    setK(newK);
                                }}
                                min="1"
                                max="99"
                                className="w-16 p-2 border rounded-lg focus:outline-none"
                            />
                        </div>

                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your message..."
                            className="flex-1 p-2 border rounded-lg focus:outline-none"
                            onKeyDown={handleKeyDown}
                        />

                        <button
                            onClick={handleSendMessage}
                            className="bg-black text-white px-4 py-2 rounded-lg hover:bg-blue-500 hover:text-white transition"
                        >
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chatbar;
