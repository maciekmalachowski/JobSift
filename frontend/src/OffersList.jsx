import React from "react"

const OffersList = ({job_offers}) => {
    return <div>
        <h2>Job Offers</h2>
        <table>
            <thead>
                <tr>
                    <th>name1</th>
                    <th>name2</th>
                    <th>name3</th>
                </tr>
            </thead>
            <tbody>
                {job_offers.map((offer) => (
                    <tr key={offer.id}>
                        <td>{offer.name1}</td>
                        <td>{offer.name2}</td>
                        <td>{offer.name3}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default OffersList