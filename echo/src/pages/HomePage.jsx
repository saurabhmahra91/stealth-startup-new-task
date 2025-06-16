import React, { useState, useEffect } from 'react'
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
    const [userId] = useState(() => {
        const saved = localStorage.getItem('user_id')
        if (saved) return saved
        const newId = crypto.randomUUID()
        localStorage.setItem('user_id', newId)
        return newId
    })

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
            setLoading(false)
        }
    }

    const handleFlush = async () => {
        await fetch(`${import.meta.env.VITE_APP_URL}/flush?user_id=${userId}`, { method: 'POST' })
        setProducts([])
        setJustification('')
        setFollowUp('')
    }

    return (
        <div className="home-page">
            <SearchBar onSearch={handleSearch} onFlush={handleFlush} />
            <ProductList products={products} />

            <JustificationFooter
                loading={loading}
                justification={justification}
                followUp={followUp}
            />

        </div>
    )
}


