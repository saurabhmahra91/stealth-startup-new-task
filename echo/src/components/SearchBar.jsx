import React, { useState } from 'react';
import TrashIcon from '../assets/icons/Trash';
import SendIcon from '../assets/icons/Send';

import './SearchBar.css'

export default function SearchBar({ onSearch, onFlush }) {
    const [query, setQuery] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (query.trim()) {
            onSearch(query)
            setQuery('')
        }
    }

    return (
        <div className="search-container">
            <form onSubmit={handleSubmit} className="search-form">
                <input
                    type="text"
                    className="search-input"
                    placeholder="What are you looking for?"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" className="send-button">
                    <SendIcon></SendIcon>
                </button>
            </form>
            <button className="flush-button" onClick={onFlush}>
                <TrashIcon></TrashIcon>
            </button>
        </div>
    )
}
