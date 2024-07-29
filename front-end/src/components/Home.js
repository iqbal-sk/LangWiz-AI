import React, { useState, useEffect } from 'react';
import './Home.css';
import axios from 'axios';

const Home = () => {
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('fr');
  const [targetLang, setTargetLang] = useState('en');
  const [feedback, setFeedback] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (submitted) {
      const timer = setTimeout(() => {
        setSubmitted(false);
        setFeedback(null);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [submitted]);

  const handleTranslate = async () => {
    let apiUrl;
    if (sourceLang === 'fr') {
      apiUrl = 'http://localhost:8000/translate-french';
    } else if (sourceLang === 'bg') {
      apiUrl = 'http://localhost:8000/translate-bulgarian';
    }

    try {
      const response = await axios.post(apiUrl, {
        text: inputText,
        source_lang: sourceLang,
        target_lang: targetLang,
      });
      const { translated_text } = response.data;
      setTranslatedText(translated_text);
      setSubmitted(false);
    } catch (error) {
      console.error('Error translating text:', error);
    }
  };

  const handleFeedback = async (type) => {
    setFeedback(type);
    setSubmitted(true);

    try {
      await axios.post('http://localhost:8000/feedback', {
        source_text: inputText,
        translated_text: translatedText,
        source_lang: sourceLang,
        target_lang: targetLang,
        feedback: type,
      });
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(translatedText);
    alert('Translated text copied to clipboard!');
  };

  const handleSave = () => {
    const blob = new Blob([translatedText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'translated_text.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleExport = () => {
    const blob = new Blob([JSON.stringify({ translatedText })], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'translated_text.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="home-container">
      <header className="header">
        <h1>LangWiz AI</h1>
        <p>Your intelligent language translation assistant</p>
      </header>
      <div className="translation-box">
        <textarea
          placeholder="Enter text to translate"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <div className="language-selection">
          <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
            <option value="fr">French</option>
            <option value="bg">Bulgarian</option>
          </select>
          <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
            <option value="en">English</option>
          </select>
        </div>
        <button onClick={handleTranslate}>Translate</button>
      </div>
      {translatedText && (
        <div className="result-box">
          <pre className="translated-text">{translatedText}</pre>
          <div className="actions">
            <button onClick={handleCopy}>Copy</button>
            <button onClick={handleSave}>Save</button>
            <button onClick={handleExport}>Export</button>
          </div>
          <div className="feedback">
            <p>How was your experience using LangWiz AI?</p>
            <div>
              <span onClick={() => handleFeedback('up')}>👍</span>
              <span onClick={() => handleFeedback('down')}>👎</span>
            </div>
          </div>
        </div>
      )}
      {submitted && (
        <div className="thank-you">
          {feedback === 'up' ? (
            <p>Thank you for your positive feedback! We're glad you enjoyed using LangWiz AI.</p>
          ) : (
            <p>Thank you for your feedback! We're sorry for any inconvenience and will strive to improve.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Home;
