import React, { useState } from 'react';
import { sendMessage } from '../services/api';
import './ChatInterface.css';
import userAvatar from '../assets/user.png';
import agentAvatar from '../assets/agent.png';

const ChatInterface: React.FC = () => {
    const [userInput, setUserInput] = useState('');
    const [messages, setMessages] = useState<{ sender: string; message: string }[]>([]);
    const [loading, setLoading] = useState(false);

    document.title = "Swee - The Airline Assistant";

    const handleSend = async () => {
        if (!userInput.trim()) return;

        const userMessage = { sender: "User", message: userInput };
        setMessages(prevMessages => [...prevMessages, userMessage]);
        setUserInput('');
        setLoading(true);

        try {
            const responseMessage = await sendMessage(userInput);
            const agentMessage = { sender: "Swee", message: responseMessage };
            setMessages(prevMessages => [...prevMessages, agentMessage]);

        } catch (error) {
            console.error("Error in handleSend:", error);
            const errorMessage = { sender: "Swee", message: "Failed to communicate with the backend. Please try again." };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") handleSend();
    };

    return (
        <div className="chat-container">
            <h1 className="title">Swee - The Airline Assistant</h1>
            <div className="chat-window">
                {messages.map((entry, index) => (
                    <div key={index} className={`message ${entry.sender === "User" ? "user" : "agent"}`}>
                        {entry.sender === "User" ? (
                            <div className="user-bubble">
                                <img src={userAvatar} alt="User" className="user-avatar" />
                                <div className="bubble-content">
                                    <div className="sender-label">You</div>
                                    <div>{entry.message}</div>
                                </div>
                            </div>
                        ) : (
                            <div className="agent-bubble">
                                <img src={agentAvatar} alt="Agent" className="agent-avatar" />
                                <div className="bubble-content">
                                    <div className="sender-label">Agent</div>
                                    <div>{entry.message}</div>
                                </div>
                            </div>
                        )}
                    </div>
                ))}
                {loading && <div className="loading">Loading...</div>}
            </div>
            <div className="input-area">
                <input 
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Type your message..."
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    );
};

export default ChatInterface;
