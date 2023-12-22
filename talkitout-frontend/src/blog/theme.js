import React, { useState, useEffect } from "react";
const ThemeToggleButton = () => {
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

  useEffect(() => {
    // Initialize theme based on OS settings if not already set in localStorage
    if (!localStorage.getItem("theme")) {
      const prefersDarkMode = window.matchMedia(
        "(prefers-color-scheme: dark)"
      ).matches;
      setTheme(prefersDarkMode ? "dark" : "light");
    }
  }, []);

  useEffect(() => {
    // Update localStorage and apply theme changes when theme state changes
    localStorage.setItem("theme", theme);
    toggleTheme();
  }, [theme]);

  const toggleTheme = () => {
    const darkModeStylesheet = document.getElementById("dark-mode-stylesheet");

    // Apply theme based on the current state
    darkModeStylesheet.disabled = theme === "light";

    // Update the icon inside the theme toggle button
    const sunIcon = document.querySelector(".theme-toggle .gg-sun");
    const moonIcon = document.querySelector(".theme-toggle .gg-moon");

    if (theme === "dark") {
      sunIcon.style.display = "none";
      moonIcon.style.display = "inline-block";
    } else {
      sunIcon.style.display = "inline-block";
      moonIcon.style.display = "none";
    }
  };

  const handleToggleClick = (e) => {
    e.preventDefault();
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  useEffect(() => {
    // Apply theme changes when component mounts
    toggleTheme();
  }, []); // Empty dependency array ensures this effect runs only once on mount
  return (
    <a
      className="nav-item nav-link theme-toggle"
      href="#"
      onClick={handleToggleClick}
    >
      <i className="gg-sun"></i>
      <i className="gg-moon" style={{ display: "none" }}></i>
    </a>
  );
};

export default ThemeToggleButton;
