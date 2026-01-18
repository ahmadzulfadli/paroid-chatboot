console.log('Script loaded!');

// 1. KONFIGURASI API (Sesuaikan dengan app.py)
const API_URL = '/api/chat'; 

/**
 * Fungsi untuk memformat angka ke Rupiah
 */
function formatRupiah(angka) {
    return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR' }).format(angka);
}

/**
 * Fungsi utama untuk menambah pesan ke Chatbox
 */
function addMessage(content, sender, type = 'text', rawData = null) {
    const messagesContainer = document.getElementById('chatMessages'); 
    const time = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }).replace('.', ':');

    if (!messagesContainer) return;

    let messageHTML = '';

    if (sender === 'user') {
        // ============================================================
        // USER BUBBLE (Kanan) - Support Dark Mode
        // ============================================================
        messageHTML = `
            <div class="flex w-full justify-end mb-4 animate-fade-in">
                <div class="max-w-[85%] md:max-w-[65%] flex flex-col items-end">
                    <div class="text-xs font-bold mb-1 text-teal-600 dark:text-teal-400">Anda</div>
                    
                    <div class="bg-teal-600 dark:bg-teal-700 text-white rounded-2xl rounded-tr-none py-3 px-4 shadow-md text-sm break-words text-right border border-teal-600 dark:border-teal-800">
                        ${escapeHtml(content)}
                        <div class="text-[10px] text-teal-100 mt-1 text-left opacity-80">${time}</div>
                    </div>
                </div>
            </div>`;
    } else {
        // ============================================================
        // BOT BUBBLE (Kiri) - Support Dark Mode
        // ============================================================
        let innerContent = '';

        if (type === 'calculation' && rawData) {
            // --------------------------------------------------------
            // RENDER TABEL PERHITUNGAN (Support Dark Mode)
            // --------------------------------------------------------
            
            // Generate Baris Tabel
            const tableRows = rawData.data.map(item => `
                <tr class="border-b border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
                    <td class="px-3 py-2 text-slate-700 dark:text-slate-300 font-medium">${item.heir} (${item.count})</td>
                    
                    <td class="px-3 py-2 text-slate-500 dark:text-slate-400 text-center text-xs font-mono bg-slate-50 dark:bg-slate-900/50 rounded">${item.fraction}</td>
                    
                    <td class="px-3 py-2 font-bold text-emerald-600 dark:text-emerald-400 text-right">${item.nominal}</td>
                </tr>
            `).join('');

            // Bungkus Tabel dengan Container
            innerContent = `
                <div class="font-bold mb-3 border-b border-slate-200 dark:border-slate-700 pb-2 text-slate-800 dark:text-slate-200 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-teal-600 dark:text-teal-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    Hasil Perhitungan Waris
                </div>
                
                <div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm">
                    <table class="w-full text-sm text-left">
                        <thead class="text-xs text-slate-200 bg-slate-800 dark:bg-slate-900 uppercase font-bold">
                            <tr>
                                <th class="px-3 py-3 border-r border-slate-700">Ahli Waris</th>
                                <th class="px-3 py-3 text-center border-r border-slate-700">Bagian</th>
                                <th class="px-3 py-3 text-right">Nominal</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
                            ${tableRows}
                        </tbody>
                    </table>
                </div>
                
                <div class="text-xs mt-3 text-slate-500 dark:text-slate-400 italic text-right flex justify-end items-center gap-1">
                    <span>Total Harta:</span>
                    <span class="font-bold text-slate-700 dark:text-slate-200">Rp ${rawData.total_harta.toLocaleString('id-ID')}</span>
                </div>
            `;
        } else {
            // Teks Biasa
            innerContent = `<div class="text-slate-700 dark:text-slate-300 leading-relaxed">${escapeHtml(content)}</div>`;
        }

        messageHTML = `
            <div class="flex w-full justify-start mb-4 animate-fade-in">
                <div class="max-w-[95%] md:max-w-[85%] flex flex-col items-start">
                    <div class="text-xs font-bold mb-1 text-teal-600 dark:text-teal-400 ml-1">Islamic Bot</div>
                    
                    <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl rounded-tl-none py-4 px-5 shadow-sm text-sm break-words w-full transition-colors duration-300">
                        ${innerContent}
                        
                        <div class="text-[10px] text-slate-400 dark:text-slate-500 mt-2 text-right border-t border-slate-100 dark:border-slate-700/50 pt-1">
                            ${time}
                        </div>
                    </div>
                </div>
            </div>`;
    }

    messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 50);
}

/**
 * Mengambil respon dari Flask API
 */
async function getResponse(userMessage) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) throw new Error('Network error');

        const data = await response.json();
        return data; 

    } catch (error) {
        console.error('Error:', error);
        return { type: 'text', message: 'Maaf, server sedang sibuk atau tidak dapat dihubungi.' };
    }
}

/**
 * Logika Pengiriman Pesan
 */
async function sendMessage() {
    const input = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    
    if (!input) return;

    const message = input.value.trim();
    if (message === '') return;

    // 1. Tampilkan pesan User
    addMessage(message, 'user');
    
    // 2. Reset Input & Loading State
    input.value = '';
    input.focus();
    if(sendButton) sendButton.disabled = true;

    // Tampilkan Loading Indicator
    const loadingDiv = document.getElementById('typingIndicator');
    if(loadingDiv) loadingDiv.classList.remove('hidden');

    // 3. Ambil data dari Bot
    const botResponse = await getResponse(message);

    // Sembunyikan Loading
    if(loadingDiv) loadingDiv.classList.add('hidden');
    if(sendButton) sendButton.disabled = false;

    // 4. Tampilkan pesan Bot
    if (botResponse.type === 'calculation') {
        addMessage(null, 'bot', 'calculation', botResponse);
    } else {
        addMessage(botResponse.message, 'bot', 'text');
    }
}

/**
 * Helper: Escape HTML
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('sendButton');
    const userInput = document.getElementById('userInput');

    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }

    if (userInput) {
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        userInput.focus();
    }
});