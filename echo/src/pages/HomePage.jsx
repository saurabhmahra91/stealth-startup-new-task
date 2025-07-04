import React, { useState, useEffect, useRef } from 'react'
import SearchBar from '../components/SearchBar'
import ProductList from '../components/ProductList'
import JustificationFooter from '../components/JustificationFooter'
import "./HomePage.css"
import mockProducts from './MockProducts'

export default function HomePage() {
    const deployment = import.meta.env.VITE_APP_ENV || "prod";
    let defaultProducts;
    let defaultJustification;
    let defaultFollowUp;
    let defaultLoading;

    if (deployment === "dev") {
        defaultProducts = mockProducts;
        defaultFollowUp = "Can you please tell me your skin type or what skin concerns you want to address with the face serum?";
        defaultJustification = "I asked the user for more information about their skin type or concerns to better tailor serum recommendations. For now, the SQL query is designed to fetch face serums but with limit 0 to avoid showing irrelevant results before gathering more user input.";
        defaultLoading = false;
    }
    else {
        defaultProducts = [];
        defaultJustification = "";
        defaultFollowUp = "";
        defaultLoading = false;
    }

    const [products, setProducts] = useState(defaultProducts)
    const [justification, setJustification] = useState(defaultJustification)
    const [followUp, setFollowUp] = useState(defaultFollowUp)
    const [conversation, setConversation] = useState([]);
    const [fetchConvTrigger, setFetchConvTrigger] = useState(true);



    const [userId] = useState(() => {
        const saved = localStorage.getItem('user_id')
        if (saved) return saved
        const newId = crypto.randomUUID()
        localStorage.setItem('user_id', newId)
        return newId
    })

    useEffect(() => {
        const fetchConversation = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_APP_URL}/conversation/${userId}`);
                if (!res.ok) throw new Error('Failed to fetch conversation');
                const data = await res.json();
                setConversation(data.conversation);
            } catch (err) {
                console.error("Error loading conversation:", err);
            }
        };

        fetchConversation();
    }, [fetchConvTrigger]);

    const [loading, setLoading] = useState(defaultLoading)

    const handleSearch = async (query) => {
        setLoading(true)
        try {
            const res = await fetch(`${import.meta.env.VITE_APP_URL}/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, user_input: query }),
            })

            if (!res.ok) throw new Error('Non-200 response')

            const data = await res.json()
            setProducts(data.products)
            setJustification(data.justification)
            setFollowUp(data.follow_up)
        } catch (error) {
            console.error('Search failed:', error)
            setJustification('')
            setFollowUp('Failed request. Can you please try with a fresh session.')
        } finally {
            setFetchConvTrigger(!fetchConvTrigger)
            setLoading(false)
        }
    }

    const handleFlush = async () => {
        await fetch(`${import.meta.env.VITE_APP_URL}/flush?user_id=${userId}`, { method: 'POST' })
        setProducts([])
        setJustification('')
        setFollowUp('')
        setFetchConvTrigger(!fetchConvTrigger)
    }

    const chatEndRef = useRef(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [conversation]);

    return (
        <div className="home-page">
            <div className="center">
                <SearchBar onSearch={handleSearch} onFlush={handleFlush} />
                <div>
                    <div className="conv">
                        <div className="chat-history">
                            {conversation.map((msg, index) => {
                                const raw = msg.content || "";
                                const justificationMatch = raw.match(/<justification>(.*?)<\/justification>/s);
                                const justification = justificationMatch?.[1]?.trim();
                                const remainder = raw.replace(/<justification>.*?<\/justification>/s, "").trim();

                                return (
                                    <div key={index} className={`message ${msg.role}`}>
                                        {justification && <div className="justification">{justification}</div>}
                                        {remainder && (
                                            <div
                                                className={`reply ${msg.role}`}
                                            >
                                                <strong>{remainder}</strong>
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                            <div ref={chatEndRef} />
                        </div>

                    </div>
                    <div className="product-list-view">
                        <ProductList products={products} />
                    </div>
                </div>

                <JustificationFooter
                    loading={loading}
                    justification={justification}
                    followUp={followUp}
                />

            </div>
        </div>
    )
}


