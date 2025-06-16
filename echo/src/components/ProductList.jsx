import React from 'react'
import './ProductList.css'

export default function ProductList({ products }) {
    if (!products.length) {
        return (
            <div className="product-list">
                <div className="default-message hello-user">
                    Hello, User!
                </div>
            </div>
        )
    }


    return (
        <div className="product-list">
            {products.map((p) => (
                <div key={p.product_id} className="product-card">
                    <div className="image-overlay">
                        <button className="add-to-cart">Add To Cart</button>
                    </div>
                    <div className="card-details">
                        <h3 className="product-name">{p.name}</h3>
                        <p className="product-category">{p.category}</p>
                        <p className="product-description">{p.description}</p>
                        <p className="product-ingredients"><strong>Top Ingredients:</strong> {p.top_ingredients}</p>
                        <p className="product-tags"><strong>Tags:</strong> {p.tags.replace(/\|/g, ', ')}</p>
                        <div className="price-margin">
                            <span className="price">${p.usd_price}</span>
                            <span className="margin">Margin: {Math.round(p.margin * 100)}%</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )

}
