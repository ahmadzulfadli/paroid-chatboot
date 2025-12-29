console.log('Script loaded!');

// API Configuration
const API_URL = 'http://127.0.0.1:5000/get';

/**
 * Check if device is mobile
 */
function isMobile() {
    return window.innerWidth <= 640;
}

/**
 * Get responsive max-width for message bubbles
 */
function getMessageMaxWidth() {
    return isMobile() ? '85%' : '65%';
}

/**
 * Get current time in HH:MM format
 */
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('id-ID', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

/**
 * Escape HTML to prevent XSS and preserve line breaks
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

/**
 * Get bot response from trained model via API
 */
async function getResponse(text1) {
    try {
        console.log('Sending message to API:', text1);
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: text1
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('API Response:', data);

        // Sesuaikan dengan response Flask Anda: { "answer": "response text" }
        if (data.answer) {
            return data.answer;
        } else {
            throw new Error('No answer in response');
        }
        
    } catch (error) {
        console.error('Error getting bot response:', error);
        return 'Maaf, terjadi kesalahan. Silakan coba lagi nanti.';
    }
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('hidden');
        
        // Scroll to bottom
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer) {
            setTimeout(() => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight + 100;
            }, 100);
        }
    }
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.add('hidden');
    }
}

/**
 * Add message to chat (Responsive Version)
 */
function addMessage(text, sender) {
    console.log('Adding message:', text, 'from:', sender);
    
    const messagesContainer = document.getElementById('chatMessages');
    
    if (!messagesContainer) {
        console.error('Messages container not found!');
        return;
    }
    
    const time = getCurrentTime();
    const maxWidth = getMessageMaxWidth();
    
    if (sender === 'user') {
        // Pesan USER - KANAN (Responsive)
        const userMessageHTML = `
            <div style="display: flex; justify-content: flex-end; width: 100%; margin-bottom: 15px;">
                <div style="max-width: ${maxWidth}; display: flex; flex-direction: column; align-items: flex-end;">
                    <div style="font-size: 11px; font-weight: bold; margin-bottom: 4px; color: #1E9679;">Anda</div>
                    <div style="display: inline-block; padding: 10px 14px; border-radius: 18px; border-bottom-right-radius: 4px; background: linear-gradient(135deg, #667eea 0%, #1E9679 100%); color: white; box-shadow: 0 3px 8px rgba(102, 126, 234, 0.3); word-wrap: break-word; overflow-wrap: break-word; word-break: break-word; hyphens: auto; max-width: 100%; font-size: 14px;">
                        ${escapeHtml(text)}
                        <div style="font-size: 9px; color: rgba(255,255,255,0.7); margin-top: 6px; text-align: right; white-space: nowrap;">${time}</div>
                    </div>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', userMessageHTML);
        
    } else {
        // Pesan BOT - KIRI (Responsive)
        const botMessageHTML = `
            <div style="display: flex; justify-content: flex-start; width: 100%; margin-bottom: 15px;">
                <div style="max-width: ${maxWidth}; display: flex; flex-direction: column; align-items: flex-start;">
                    <div style="font-size: 11px; font-weight: bold; margin-bottom: 4px; color: #2563eb;">Bot</div>
                    <div style="display: inline-block; padding: 10px 14px; border-radius: 18px; border-bottom-left-radius: 4px; background: white; color: #333; box-shadow: 0 2px 6px rgba(0,0,0,0.08); border: 1px solid #e5e7eb; word-wrap: break-word; overflow-wrap: break-word; word-break: break-word; hyphens: auto; max-width: 100%; font-size: 14px;">
                        ${escapeHtml(text)}
                        <div style="font-size: 9px; color: #9ca3af; margin-top: 6px; text-align: right; white-space: nowrap;">${time}</div>
                    </div>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', botMessageHTML);
    }
    
    // Add separator
    const separatorHTML = `
        <div style="height: 1px; margin: 15px 0; background: linear-gradient(to right, transparent, #ddd, transparent);"></div>
    `;
    messagesContainer.insertAdjacentHTML('beforeend', separatorHTML);
    
    // Scroll to bottom smoothly
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 50);
}

/**
 * Send message function
 */
async function sendMessage() {
    console.log('Send button clicked!');
    
    const input = document.getElementById('userInput');
    
    if (!input) {
        console.error('Input not found!');
        return;
    }
    
    const message = input.value.trim();
    
    console.log('Message value:', message);
    
    if (message === '') {
        console.log('Empty message, not sending');
        return;
    }

    // Add user message
    addMessage(message, 'user');
    
    // Clear input
    input.value = '';
    input.focus();

    // Show typing indicator
    showTypingIndicator();

    // Get bot response from API
    const botResponse = await getResponse(message);
    
    // Hide typing indicator
    hideTypingIndicator();
    
    // Add bot response
    addMessage(botResponse, 'bot');
}

/**
 * Update message bubbles on window resize
 */
function handleResize() {
    console.log('Window resized, updating message widths');
    const messageContainers = document.querySelectorAll('#chatMessages > div > div');
    const maxWidth = getMessageMaxWidth();
    
    messageContainers.forEach(container => {
        if (container.style.maxWidth) {
            container.style.maxWidth = maxWidth;
        }
    });
}

/**
 * Initialize chatbot
 */
function init() {
    console.log('Initializing chatbot...');
    
    // Set initial time
    const initialTime = document.getElementById('initialTime');
    if (initialTime) {
        initialTime.textContent = getCurrentTime();
    }
    
    // Get elements
    const sendButton = document.getElementById('sendButton');
    const userInput = document.getElementById('userInput');
    
    console.log('Send button:', sendButton);
    console.log('User input:', userInput);
    
    // Add click event to send button
    if (sendButton) {
        sendButton.onclick = function() {
            console.log('Button clicked via onclick');
            sendMessage();
        };
        console.log('Send button event attached');
    } else {
        console.error('Send button not found!');
    }
    
    // Add keypress event to input
    if (userInput) {
        userInput.onkeypress = function(event) {
            if (event.key === 'Enter') {
                console.log('Enter pressed');
                sendMessage();
            }
        };
        userInput.focus();
        console.log('Input event attached');
    } else {
        console.error('User input not found!');
    }
    
    // Add resize event listener for responsive updates
    window.addEventListener('resize', handleResize);
    console.log('Resize handler attached');
    
    console.log('Chatbot initialized successfully!');
    console.log('Device type:', isMobile() ? 'Mobile' : 'Desktop');
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}