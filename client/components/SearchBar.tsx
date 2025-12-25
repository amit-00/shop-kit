'use client';
import { useState, useEffect } from 'react';

export default function SearchBar() {
  const [ctrlButton, setCtrlButton] = useState<string>('');
  
  useEffect(() => {
    const ctrlButton = window.navigator.userAgent.includes('Macintosh') ? '⌘' : 'Ctrl';
    setCtrlButton(ctrlButton);
  }, []);
  
  return (
    <button className="btn btn-ghost w-56 flex items-center justify-between border border-base-300 bg-base-300 hover:border-base-content/20">
      <div className="flex items-center justify-start">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-base-content/60">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <span className="text-sm ml-2 text-base-content/60">Search</span>
      </div>
      
      <span className="text-sm ml-2 text-base-content/60">{`${ctrlButton} + K`}</span>
    </button>
  );
}