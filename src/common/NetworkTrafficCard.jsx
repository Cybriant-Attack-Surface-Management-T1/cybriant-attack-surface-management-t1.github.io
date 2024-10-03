import React from 'react';

function NetworkTrafficCard({src, link, h3 }) {
  return (
    <a href={link} target="_blank">
        <h3>{h3}</h3>
        <p><strong>Traffic Volume:</strong> 15 GB in the last 24 hours</p>
        <p><strong>Peak Traffic:</strong> 5 GB at 2:00 PM</p>
        <p><strong>Suspicious Activity:</strong> Detected 3 unusual spikes</p>
    </a>
  );
};

export default NetworkTrafficCard;