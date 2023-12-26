import React from 'react';

const NotFound = () => {
  return (
    <div style={styles.body}>
      <div style={styles.container}>
        <div style={styles.icon}>
          <i className="fas fa-exclamation-circle"></i>
        </div>
        <h1 style={styles.h1}>404 - Page Not Found</h1>
        <p style={styles.p}>Sorry, the page you are looking for does not exist.</p>
        <p style={styles.p}>
          <a href="/"><b style={styles.b}>Go back to the home page</b></a>
        </p>
      </div>
    </div>
  );
};

const styles = {
  body: {
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f5f5f5',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    margin: 0,
  },
  container: {
    textAlign: 'center',
    padding: '20px',
    borderRadius: '8px',
    backgroundColor: '#fff',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  },
  icon: {
    fontSize: '80px',
    color: '#f44336',
    marginBottom: '20px',
  },
  h1: {
    color: '#333',
    marginBottom: '10px',
  },
  p: {
    color: '#666',
    marginBottom: '20px',
  },
  a: {
    color: '#2196F3',
    textDecoration: 'none',
    fontWeight: 'bold',
  },
  b:{
   color:'blue',
  },
};

export default NotFound;