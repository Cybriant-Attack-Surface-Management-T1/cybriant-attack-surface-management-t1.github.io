import React from 'react';

function SslDnsStatusCard({src, link, h3 }) {
  return (
    <a href={link} target="_blank">
        <h3>{h3}</h3>
        <p><strong>SSL Certificates:</strong> All valid</p>
        <p><strong>DNS Vulnerabilities:</strong> 1 misconfigured entry</p>
    </a>
  );
};

export default SslDnsStatusCard;