import React, { useState, useEffect, useRef } from 'react';
import { api, baseURL } from './api';
import { useNavigate } from 'react-router-dom';
import Loader from './Loader'; // Import the Loader component
import ReactMarkdown from 'react-markdown';

const Chat = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chatHistoryLoading, setChatHistoryLoading] = useState(true);
  const access_token = localStorage.getItem('access_token');
  const navigate = useNavigate();
  const chatContainerRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  const fetchChatHistory = async () => {
    try {
      setChatHistoryLoading(true);
      const response = await api.get('/medbot/chat-history/', {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      setMessages(response.data.data);
    } catch (error) {
      console.error(error);
    } finally {
      setChatHistoryLoading(false);
    }
  };

  const handleQuerySubmit = async () => {
    if (!query.trim()) {
      return;
    }
    setLoading(true);
    setMessages(prevMessages => [...prevMessages, { type: 'human', content: query }]);
    scrollToBottom();
    setQuery('');
    try {
      const response = await fetch(`${baseURL}/medbot/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${access_token}`
        },
        body: JSON.stringify({ query }),
        cache: 'no-cache'
      });

      if (!response.ok || !response.body) {
        throw new Error('Network response was not ok');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let done = false;
      let text = '';

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunkValue = decoder.decode(value);
        console.log(chunkValue);
        text += chunkValue;
        setMessages(prevMessages => {
          const lastMessage = prevMessages[prevMessages.length - 1];
          if (lastMessage.type === 'ai') {
            return [
              ...prevMessages.slice(0, -1),
              { type: 'ai', content: text }
            ];
          } else {
            return [
              ...prevMessages,
              { type: 'ai', content: text }
            ];
          }
        });
        scrollToBottom();
      }

      setQuery('');
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = async () => {
    try {
      await api.get('/medbot/clear-chat/', {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      setMessages([]);
      fetchChatHistory();
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    navigate('/signin');
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h2 className="text-2xl mb-4">Chat</h2>
      <div className="w-full max-w-2xl bg-white p-4 rounded-lg shadow-md overflow-y-auto" ref={chatContainerRef} style={{ maxHeight: '60vh' }}>
        {chatHistoryLoading ? (
          <div className="flex justify-center items-center h-full">
            <Loader />
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`mb-2 ${message.type === 'human' ? 'text-right' : 'text-left'}`}>
              <div className={`inline-block px-4 py-2 rounded-lg ${message.type === 'human' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
                {message.type === 'ai' ? (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                ) : (
                  message.content
                )}
              </div>
            </div>
          ))
        )}
      </div>
      <div className="w-full max-w-2xl flex mt-4">
        <input
          type="text"
          id="queryInput"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="px-4 py-2 border rounded-md w-full"
        />
        <button
          onClick={handleQuerySubmit}
          className="px-4 py-2 ml-2 bg-blue-500 text-white rounded-md"
          disabled={loading}
        >
          {loading ? <Loader /> : 'Send'}
        </button>
      </div>
      <button
        onClick={handleClearChat}
        className="absolute top-4 left-4 px-4 py-2 bg-red-500 text-white rounded-md"
      >
        Clear Chat
      </button>
      <button
        onClick={handleLogout}
        className="absolute top-4 right-4 px-4 py-2 bg-gray-500 text-white rounded-md"
      >
        Logout
      </button>
    </div>
  );
};

export default Chat;