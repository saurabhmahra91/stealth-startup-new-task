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
                <div key={p.id} className="product-card">
                    <div className="image-overlay">
                        <button className="add-to-cart">Add To Cart</button>
                    </div>
                    <div className="card-details">
                        <h3 className="product-name">{p.name}</h3>
                        <p className="product-category">{p.category}</p>
                        <p className="product-sizes"><strong>Sizes:</strong> {p.available_sizes.join(', ')}</p>
                        <p className="product-fabric"><strong>Fabric:</strong> {p.fabric}</p>
                        <p className="product-fit"><strong>Fit:</strong> {p.fit}</p>
                        <p className="product-sleeve"><strong>Sleeve:</strong> {p.sleeve_length}</p>
                        <p className="product-color"><strong>Color/Print:</strong> {p.color_or_print}</p>
                        <div className="price-margin">
                            <span className="price">${p.usd_price}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
