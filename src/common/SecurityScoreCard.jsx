import React from 'react';

function SecurityScoreCard({src, link, h3, p }) {
  return (
    <a href={link} target="_blank">
        <h3>{h3}</h3>
        <p>{p}</p>
        <img className="hover" src={src} alt={`${h3} logo`} />
    </a>
  );
};

export default SecurityScoreCard;