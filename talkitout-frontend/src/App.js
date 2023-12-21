// Importing the logo image from the 'logo.svg' file
import logo from './logo.svg';
// Importing styles from the 'App.css' file
import './App.css';

// Functional component for the main App
function App() {
  return (
    // Main container div with class 'App'
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

// Exporting the App component as the default export of the module
export default App;
