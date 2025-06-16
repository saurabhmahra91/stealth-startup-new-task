import React, { useEffect, useState } from 'react'
import AgentIcon from '../assets/icons/Brain'
import './JustificationFooter.css'

const MEAN_CHAR_DELAY = 50;
const MEAN_CHAR_JITTER_VARIANCE = 100;
const randomDelay = (mean, variance) => {
    const stdDev = Math.sqrt(variance)
    const gaussian = () => {
        // Box-Muller transform for normal-ish distribution
        let u = 0, v = 0
        while (u === 0) u = Math.random()
        while (v === 0) v = Math.random()
        return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v)
    }

    const delay = Math.max(10, mean + gaussian() * stdDev)
    return delay
}


export default function JustificationFooter({ justification = '', followUp = '', loading }) {
    const [typedJustification, setTypedJustification] = useState('')
    const [typedFollowUp, setTypedFollowUp] = useState('')
    const [isTypingJustification, setIsTypingJustification] = useState(false)
    const [isTypingFollowUp, setIsTypingFollowUp] = useState(false)

    useEffect(() => {
        if (!loading && justification) {
            setTypedJustification('')
            setIsTypingJustification(true)
            let index = 0
            const typeNextChar = () => {
                setTypedJustification(justification.slice(0, index + 1))
                index++
                if (index < justification.length) {
                    setTimeout(typeNextChar, randomDelay(MEAN_CHAR_DELAY, MEAN_CHAR_JITTER_VARIANCE))
                } else {
                    setIsTypingJustification(false)
                }
            }
            setTimeout(typeNextChar, randomDelay(MEAN_CHAR_DELAY, MEAN_CHAR_JITTER_VARIANCE))
        }
    }, [justification, loading])

    useEffect(() => {
        if (!loading && followUp) {
            setTypedFollowUp('')
            setIsTypingFollowUp(true)
            let index = 0
            const typeNextChar = () => {
                setTypedFollowUp(followUp.slice(0, index + 1))
                index++
                if (index < followUp.length) {
                    setTimeout(typeNextChar, randomDelay(MEAN_CHAR_DELAY, MEAN_CHAR_JITTER_VARIANCE))
                } else {
                    setIsTypingFollowUp(false)
                }
            }
            setTimeout(typeNextChar, randomDelay(MEAN_CHAR_DELAY, MEAN_CHAR_JITTER_VARIANCE))
        }
    }, [followUp, loading])


    const [dots, setDots] = useState('.')

    useEffect(() => {
        if (loading) {
            const interval = setInterval(() => {
                setDots(prev => (prev.length === 3 ? '.' : prev + '.'))
            }, 500)
            return () => clearInterval(interval)
        }
    }, [loading])


    return (
        <footer className="justification-footer">
            {loading ? (
                <div className="thinking-loader">
                    <AgentIcon className="agent-icon" />
                    <span className="thinking-dots">{dots}</span>
                </div>
            ) : (
                <div className="typing-wrapper">
                    {followUp && (
                        <p className="follow-up-line">
                            <AgentIcon className="agent-icon" /> {typedFollowUp}
                        </p>
                    )}
                    {justification && (
                        <p className="justification-line">
                            &gt; {typedJustification}
                        </p>
                    )}
                </div>
            )}
        </footer>
    )
}
