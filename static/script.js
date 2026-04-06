document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const messagesContainer = document.getElementById('messages');

    const languageBtn = document.getElementById('language-btn');
    const languageDropdown = document.getElementById('language-dropdown');
    const currentLanguageFlag = document.getElementById('current-language-flag');
    const currentLanguageName = document.getElementById('current-language-name');
    const languageOptions = document.querySelectorAll('.language-option');

    let currentLanguage = localStorage.getItem('preferred_language') || 'en';

    const languageData = {
        'en': { flag: '🇬🇧', name: 'English' },
        'hi': { flag: '🇮🇳', name: 'हिंदी' },
        'ta': { flag: '🇮🇳', name: 'தமிழ்' },
        'te': { flag: '🇮🇳', name: 'తెలుగు' },
        'bn': { flag: '🇮🇳', name: 'বাংলা' },
        'mr': { flag: '🇮🇳', name: 'मराठी' },
        'gu': { flag: '🇮🇳', name: 'ગુજરાતી' }
    };

    const profileBtn = document.getElementById('profile-btn');
    const profileModal = document.getElementById('profile-modal');
    const closeBtn = document.querySelector('.close');
    const cancelBtn = document.getElementById('cancel-btn');
    const profileForm = document.getElementById('profile-form');

    const statsBtn = document.getElementById('stats-btn');
    const statsModal = document.getElementById('stats-modal');
    const closeStatsBtn = document.querySelector('.close-stats');

    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.querySelector('.close-settings');
    const themeToggle = document.getElementById('theme-toggle');
    const notificationsToggle = document.getElementById('notifications-toggle');
    const dataSharingToggle = document.getElementById('data-sharing-toggle');
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    const exportDataBtn = document.getElementById('export-data-btn');

    const hospitalModal = document.getElementById('hospital-modal');
    const closeHospitalBtn = document.querySelector('.close-hospital');
    const findHospitalsBtn = document.getElementById('find-hospitals-btn');
    const hospitalsList = document.getElementById('hospitals-list');

    const pharmacyBtn = document.getElementById('pharmacy-btn');
    const pharmacyModal = document.getElementById('pharmacy-modal');
    const closePharmacyBtn = document.querySelector('.close-pharmacy');
    const pharmaciesList = document.getElementById('pharmacies-list');

    const wellnessBtn = document.getElementById('wellness-btn');
    const wellnessModal = document.getElementById('wellness-modal');
    const closeWellnessBtn = document.querySelector('.close-wellness');

    const prescriptionsBtn = document.getElementById('prescriptions-btn');
    const prescriptionsModal = document.getElementById('prescriptions-modal');
    const closePrescriptionsBtn = document.querySelector('.close-prescriptions');
    const prescriptionUploadForm = document.getElementById('prescription-upload-form');
    const prescriptionFileInput = document.getElementById('prescription-file');
    const filePreview = document.getElementById('file-preview');
    const previewImage = document.getElementById('preview-image');
    const prescriptionsList = document.getElementById('prescriptions-list');

    const labTestsBtn = document.getElementById('lab-tests-btn');
    const labTestsModal = document.getElementById('lab-tests-modal');
    const closeLabTestsBtn = document.querySelector('.close-lab-tests');
    const labReportUploadForm = document.getElementById('lab-report-upload-form');
    const labReportFileInput = document.getElementById('lab-report-file');
    const labFilePreview = document.getElementById('lab-file-preview');
    const labPreviewImage = document.getElementById('lab-preview-image');
    const labReportsList = document.getElementById('lab-reports-list');
    const labAnalysisSection = document.getElementById('lab-analysis-section');
    const closeAnalysisBtn = document.getElementById('close-analysis-btn');
    const labChatForm = document.getElementById('lab-chat-form');
    const labChatInput = document.getElementById('lab-chat-input');
    const labChatMessages = document.getElementById('lab-chat-messages');

    let currentLabReportId = null;

    const totalPointsEl = document.getElementById('total-points');
    const totalBadgesEl = document.getElementById('total-badges');

    const nutritionBtn = document.getElementById('nutrition-btn');
    const nutritionModal = document.getElementById('nutrition-modal');
    const closeNutritionBtn = document.querySelector('.close-nutrition');
    const foodScannerForm = document.getElementById('food-scanner-form');
    const foodImageInput = document.getElementById('food-image');
    const foodPreviewContainer = document.getElementById('food-preview-container');
    const foodPreviewImage = document.getElementById('food-preview');
    const foodScanResult = document.getElementById('food-scan-result');
    const receiptAuditorForm = document.getElementById('receipt-auditor-form');
    const receiptImageInput = document.getElementById('receipt-image');
    const receiptPreviewContainer = document.getElementById('receipt-preview-container');
    const receiptPreviewImage = document.getElementById('receipt-preview');
    const receiptAuditResult = document.getElementById('receipt-audit-result');

    const insuranceBtn = document.getElementById('insurance-btn');
    const insuranceModal = document.getElementById('insurance-modal');
    const closeInsuranceBtn = document.querySelector('.close-insurance');
    const checkInsuranceBtn = document.getElementById('check-insurance-btn');
    const policyTextInput = document.getElementById('policy-text');
    const treatmentNameInput = document.getElementById('treatment-name');
    const insuranceResult = document.getElementById('insurance-result');

    const firstAidBtn = document.getElementById('first-aid-btn');
    const firstAidModal = document.getElementById('first-aid-modal');
    const closeFirstAidBtn = document.querySelector('.close-first-aid');
    const firstAidChips = document.querySelectorAll('.first-aid-chip');

    const viewLabTrendsBtn = document.getElementById('view-lab-trends-btn');
    const labTrendsSection = document.getElementById('lab-trends-section');
    const closeTrendsBtn = document.getElementById('close-trends-btn');

    const digitalTwinBtn = document.getElementById('digital-twin-btn');
    const digitalTwinModal = document.getElementById('digital-twin-modal');
    const closeDigitalTwinBtn = document.querySelector('.close-digital-twin');

    const symptomCamBtn = document.getElementById('symptom-cam-btn');
    const symptomCamModal = document.getElementById('symptom-cam-modal');
    const closeSymptomCamBtn = document.querySelector('.close-symptom-cam');
    const symptomCamForm = document.getElementById('symptom-cam-form');
    const symptomImageInput = document.getElementById('symptom-image');
    const symptomFilePreview = document.getElementById('symptom-file-preview');
    const symptomPreviewImage = document.getElementById('symptom-preview-image');
    const symptomCamResult = document.getElementById('symptom-cam-result');
    const symptomContext = document.getElementById('symptom-context');

    const verifyMedSafetyBtn = document.getElementById('verify-med-safety-btn');

    const emergencyAlert = document.getElementById('emergency-alert');

    // --- CRITICAL FIRST AID HANDLER (TOP PRIORITY) ---
    const firstAidSelector = document.querySelector('.first-aid-selector');
    if (firstAidSelector) {
        console.log("First Aid selector found, attaching listener");
        firstAidSelector.addEventListener('click', async (e) => {
            const chip = e.target.closest('.first-aid-chip');
            if (!chip) return;

            const type = chip.dataset.type;
            console.log("First Aid chip clicked:", type);
            const stepsDiv = document.getElementById('first-aid-steps');
            if (!stepsDiv) return;

            stepsDiv.innerHTML = '<div style="padding: 20px; text-align: center;"><i class="fas fa-spinner fa-spin"></i> Loading life-saving steps...</div>';

            try {
                const res = await fetch(`/first-aid?type=${type}&_t=${Date.now()}`);
                if (!res.ok) throw new Error(`Server error: ${res.status}`);
                const data = await res.json();

                if (data.steps && Array.isArray(data.steps)) {
                    stepsDiv.innerHTML = data.steps.map(s => `
                        <div class="step" style="margin-bottom: 12px; padding: 15px; border-left: 5px solid var(--primary-color); background: #ffffff; border-radius: 0 10px 10px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); color: #1e293b; display: block!important;">
                            <div style="font-weight: 700; color: var(--primary-color); margin-bottom: 5px; font-size: 0.8rem; text-transform: uppercase;">Step ${s.step}</div>
                            <div style="line-height: 1.5;">${s.text}</div>
                        </div>`).join('');
                } else {
                    stepsDiv.innerHTML = '<div class="no-data">Invalid data received from server.</div>';
                }

                document.querySelectorAll('.first-aid-chip').forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
            } catch (err) {
                console.error("First Aid fetch error:", err);
                stepsDiv.innerHTML = `<div class="no-data" style="color: #dc2626; padding: 20px;"><strong>Error:</strong> ${err.message}. Please check server logs.</div>`;
            }
        });
    }

    initializeLanguage();

    loadProfile();
    loadSettings();

    function initializeLanguage() {
        loadUserLanguage();
        updateLanguageDisplay();
    }

    async function loadUserLanguage() {
        try {
            const response = await fetch('/get-language?user_id=default');
            const data = await response.json();
            if (data.language) {
                currentLanguage = data.language;
                localStorage.setItem('preferred_language', currentLanguage);
                updateLanguageDisplay();
            }
        } catch (error) {
            console.error('Error loading language:', error);
        }
    }

    function updateLanguageDisplay() {
        const lang = languageData[currentLanguage] || languageData['en'];
        currentLanguageFlag.textContent = lang.flag;
        currentLanguageName.textContent = lang.name;

        languageOptions.forEach(option => {
            if (option.dataset.lang === currentLanguage) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }

    languageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isVisible = languageDropdown.style.display === 'block';
        languageDropdown.style.display = isVisible ? 'none' : 'block';
        languageBtn.classList.toggle('active', !isVisible);
    });

    document.addEventListener('click', (e) => {
        if (!languageBtn.contains(e.target) && !languageDropdown.contains(e.target)) {
            languageDropdown.style.display = 'none';
            languageBtn.classList.remove('active');
        }
    });

    languageOptions.forEach(option => {
        option.addEventListener('click', async () => {
            const selectedLang = option.dataset.lang;
            if (selectedLang !== currentLanguage) {
                await setLanguage(selectedLang);
            }
            languageDropdown.style.display = 'none';
            languageBtn.classList.remove('active');
        });
    });

    async function setLanguage(lang) {
        try {
            const response = await fetch('/set-language', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: 'default',
                    language: lang
                })
            });

            const data = await response.json();
            if (data.success) {
                currentLanguage = lang;
                localStorage.setItem('preferred_language', lang);
                updateLanguageDisplay();

                const langName = languageData[lang].name;
                addMessage(`Language changed to ${langName}`, 'bot');
            }
        } catch (error) {
            console.error('Error setting language:', error);
        }
    }


    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message,
                    user_id: 'default',
                    language: currentLanguage
                })
            });

            const data = await response.json();

            if (data.error) {
                addMessage('Error: ' + data.error, 'bot');
            } else {
                // Check for emergency
                if (data.is_emergency) {
                    showEmergencyAlert();

                    // Auto open hospital locator
                    if (typeof openHospitalLocator === 'function') {
                        openHospitalLocator();
                    }

                    addMessage(data.response, 'bot', null);

                    if (data.emergency_guidance) {
                        const guidance = data.emergency_guidance;
                        const guidanceHtml = `
                            <div class="emergency-guidance-card">
                                <p><strong><i class="fas fa-exclamation-circle"></i> Primary Action:</strong> ${guidance.primary_action}</p>
                                <ul style="text-align: left; margin-top: 0.5rem;">
                                    ${guidance.general_instructions.map(i => `<li>${i}</li>`).join('')}
                                </ul>
                                <div style="margin-top: 0.5rem;">
                                    <strong>Emergency Contacts:</strong><br>
                                    Ambulance: <a href="tel:${guidance.contacts.ambulance}">${guidance.contacts.ambulance}</a><br>
                                    Police: <a href="tel:${guidance.contacts.police}">${guidance.contacts.police}</a>
                                </div>
                            </div>
                        `;
                        addMessage(guidanceHtml, 'bot', null, true);
                    }
                } else {
                    // Check for symptom analysis emergency (legacy check)
                    if (data.symptom_analysis && data.symptom_analysis.is_emergency) {
                        showEmergencyAlert();
                    }
                    // Add bot response with risk badge if symptoms detected
                    addMessage(data.response, 'bot', data.symptom_analysis);
                }
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
        }
    });

    function addMessage(text, sender, symptomAnalysis = null, isHtml = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');

        if (isHtml) {
            bubbleDiv.innerHTML = text;
        } else if (sender === 'bot') {
            // Parse Markdown for bot messages
            bubbleDiv.innerHTML = marked.parse(text);
        } else {
            bubbleDiv.textContent = text;
        }

        // Add risk badge if symptoms detected
        if (symptomAnalysis && symptomAnalysis.has_symptoms && symptomAnalysis.risk_level !== 'none') {
            const riskBadge = document.createElement('span');
            riskBadge.classList.add('risk-badge', `risk-${symptomAnalysis.risk_level}`);
            riskBadge.textContent = symptomAnalysis.risk_level;
            bubbleDiv.appendChild(riskBadge);
        }

        messageDiv.appendChild(bubbleDiv);
        messagesContainer.appendChild(messageDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Profile modal functionality
    profileBtn.addEventListener('click', (e) => {
        e.preventDefault();
        profileModal.classList.add('show');
    });

    closeBtn.addEventListener('click', () => {
        profileModal.classList.remove('show');
    });

    cancelBtn.addEventListener('click', () => {
        profileModal.classList.remove('show');
    });

    // Close modal when clicking outside
    profileModal.addEventListener('click', (e) => {
        if (e.target === profileModal) {
            profileModal.classList.remove('show');
        }
    });

    // Load profile from server
    async function loadProfile() {
        try {
            const response = await fetch('/profile?user_id=default');
            const profile = await response.json();

            // Populate form fields
            document.getElementById('age').value = profile.age || '';
            document.getElementById('conditions').value = profile.conditions ? profile.conditions.join(', ') : '';
            document.getElementById('allergies').value = profile.allergies ? profile.allergies.join(', ') : '';
            document.getElementById('medications').value = profile.medications ? profile.medications.join(', ') : '';
            document.getElementById('goals').value = profile.goals ? profile.goals.join(', ') : '';
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }

    // Save profile
    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            user_id: 'default',
            age: parseInt(document.getElementById('age').value) || null,
            conditions: document.getElementById('conditions').value.split(',').map(s => s.trim()).filter(s => s),
            allergies: document.getElementById('allergies').value.split(',').map(s => s.trim()).filter(s => s),
            medications: document.getElementById('medications').value.split(',').map(s => s.trim()).filter(s => s),
            goals: document.getElementById('goals').value.split(',').map(s => s.trim()).filter(s => s)
        };

        try {
            const response = await fetch('/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                profileModal.classList.remove('show');
                addMessage('Profile updated successfully! Your health recommendations will now be personalized.', 'bot');
            } else {
                alert('Error saving profile. Please try again.');
            }
        } catch (error) {
            console.error('Error saving profile:', error);
            alert('Error saving profile. Please try again.');
        }
    });

    // Stats modal functionality
    statsBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await loadStats();
        statsModal.classList.add('show');
    });

    closeStatsBtn.addEventListener('click', () => {
        statsModal.classList.remove('show');
    });

    statsModal.addEventListener('click', (e) => {
        if (e.target === statsModal) {
            statsModal.classList.remove('show');
        }
    });

    async function loadStats() {
        try {
            const response = await fetch('/stats?user_id=default');
            const stats = await response.json();

            // Update stat cards
            document.getElementById('total-chats').textContent = stats.total_conversations;
            document.getElementById('profile-completion').textContent = stats.profile_completion + '%';

            const healthItems = stats.health_profile.conditions_count +
                stats.health_profile.allergies_count +
                stats.health_profile.medications_count +
                stats.health_profile.goals_count;
            document.getElementById('health-items').textContent = healthItems;

            // Update topics list
            const topicsList = document.getElementById('topics-list');
            if (Object.keys(stats.topics).length > 0) {
                topicsList.innerHTML = '';
                for (const [topic, count] of Object.entries(stats.topics)) {
                    const topicItem = document.createElement('div');
                    topicItem.className = 'topic-item';
                    topicItem.innerHTML = `
                        <span class="topic-name">${topic}</span>
                        <span class="topic-count">${count} conversation${count > 1 ? 's' : ''}</span>
                    `;
                    topicsList.appendChild(topicItem);
                }
            } else {
                topicsList.innerHTML = '<p class="no-data">No conversations yet. Start chatting to see your topics!</p>';
            }

            // Update recent conversations
            const recentList = document.getElementById('recent-list');
            if (stats.recent_interactions.length > 0) {
                recentList.innerHTML = '';
                stats.recent_interactions.forEach(interaction => {
                    const recentItem = document.createElement('div');
                    recentItem.className = 'recent-item';
                    const date = new Date(interaction.timestamp);
                    recentItem.innerHTML = `
                        <div class="recent-header">
                            <span class="recent-topic">${interaction.topic}</span>
                            <span class="recent-time">${formatDate(date)}</span>
                        </div>
                        <p class="recent-message">${truncate(interaction.message, 80)}</p>
                    `;
                    recentList.appendChild(recentItem);
                });
            } else {
                recentList.innerHTML = '<p class="no-data">No recent conversations</p>';
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    // Settings modal functionality
    settingsBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await loadSettings();
        settingsModal.classList.add('show');
    });

    closeSettingsBtn.addEventListener('click', () => {
        settingsModal.classList.remove('show');
    });

    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.remove('show');
        }
    });

    async function loadSettings() {
        try {
            const response = await fetch('/settings?user_id=default');
            const settings = await response.json();

            // Update toggles
            themeToggle.checked = settings.theme === 'dark';
            notificationsToggle.checked = settings.notifications;
            dataSharingToggle.checked = settings.data_sharing;

            // Apply theme
            if (settings.theme === 'dark') {
                document.body.classList.add('dark-mode');
            }
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }

    async function saveSettings() {
        const settings = {
            theme: themeToggle.checked ? 'dark' : 'light',
            notifications: notificationsToggle.checked,
            data_sharing: dataSharingToggle.checked
        };

        try {
            await fetch('/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: 'default',
                    settings: settings
                })
            });
        } catch (error) {
            console.error('Error saving settings:', error);
        }
    }

    // Theme toggle
    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
        saveSettings();
    });

    // Other settings toggles
    notificationsToggle.addEventListener('change', saveSettings);
    dataSharingToggle.addEventListener('change', saveSettings);

    // Clear history
    clearHistoryBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to clear all chat history? This action cannot be undone.')) {
            try {
                const response = await fetch('/clear-history', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: 'default'
                    })
                });

                const data = await response.json();
                if (data.success) {
                    alert('Chat history cleared successfully!');
                    // Reload stats
                    await loadStats();
                }
            } catch (error) {
                console.error('Error clearing history:', error);
                alert('Error clearing history. Please try again.');
            }
        }
    });

    // Export data
    exportDataBtn.addEventListener('click', async () => {
        try {
            const [profileRes, statsRes] = await Promise.all([
                fetch('/profile?user_id=default'),
                fetch('/stats?user_id=default')
            ]);

            const profile = await profileRes.json();
            const stats = await statsRes.json();

            const exportData = {
                profile: profile,
                statistics: stats,
                exported_at: new Date().toISOString()
            };

            const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `health-data-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error exporting data:', error);
            alert('Error exporting data. Please try again.');
        }
    });

    // Helper functions
    function formatDate(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;
        return date.toLocaleDateString();
    }

    function truncate(str, length) {
        return str.length > length ? str.substring(0, length) + '...' : str;
    }

    // Emergency Alert Functions
    function showEmergencyAlert() {
        emergencyAlert.style.display = 'block';
    }

    function hideEmergencyAlert() {
        emergencyAlert.style.display = 'none';
    }

    // Close emergency alert button
    const closeEmergencyBtn = document.getElementById('close-emergency-alert');
    if (closeEmergencyBtn) {
        closeEmergencyBtn.addEventListener('click', hideEmergencyAlert);
    }

    // Hospital Locator Functions
    findHospitalsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openHospitalLocator();
    });

    closeHospitalBtn.addEventListener('click', () => {
        hospitalModal.classList.remove('show');
    });

    hospitalModal.addEventListener('click', (e) => {
        if (e.target === hospitalModal) {
                    hospitalModal.classList.remove('show');
        }
    });

    // Nutrition Modal Functions
    nutritionBtn.addEventListener('click', (e) => {
        e.preventDefault();
        nutritionModal.classList.add('show');
    });

    if (closeNutritionBtn) closeNutritionBtn.addEventListener('click', () => {
        nutritionModal.classList.remove('show');
    });

    if (nutritionModal) nutritionModal.addEventListener('click', (e) => {
        if (e.target === nutritionModal) nutritionModal.classList.remove('show');
    });

    // --- Nutrition Hub Vision-AI Handling ---

    // Food Scanner Preview
    if (foodImageInput) {
        foodImageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    foodPreviewImage.src = e.target.result;
                    foodPreviewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                foodPreviewContainer.style.display = 'none';
            }
        });
    }

    // Food Scanner Submission
    if (foodScannerForm) {
        foodScannerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const file = foodImageInput.files[0];
            if (!file) {
                alert('Please select an image of the ingredient list.');
                return;
            }

            const formData = new FormData();
            formData.append('image', file);
            formData.append('user_id', 'default');

            const submitBtn = foodScannerForm.querySelector('button[type="submit"]');
            const originalBtnContent = submitBtn.innerHTML;

            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Auditing...';
            submitBtn.disabled = true;
            foodScanResult.style.display = 'block';
            foodScanResult.innerHTML = '<div style="text-align: center; padding: 15px;"><i class="fas fa-spinner fa-spin"></i> FSSAI Auditor is checking ingredients...</div>';

            try {
                const res = await fetch('/scan-food', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (data.status === 'success') {
                    renderFoodScanResult(data);
                } else {
                    foodScanResult.innerHTML = `<div style="color: #dc2626; padding: 10px; background: #fee2e2; border-radius: 8px;">Error: ${data.message}</div>`;
                }
            } catch (err) {
                console.error("Food Scan Error:", err);
                foodScanResult.innerHTML = `<div style="color: #dc2626; padding: 10px; background: #fee2e2; border-radius: 8px;">Error: ${err.message}</div>`;
            } finally {
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
            }
        });
    }

    // Receipt Auditor Preview
    if (receiptImageInput) {
        receiptImageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    receiptPreviewImage.src = e.target.result;
                    receiptPreviewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                receiptPreviewContainer.style.display = 'none';
            }
        });
    }

    // Receipt Auditor Submission
    if (receiptAuditorForm) {
        receiptAuditorForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const file = receiptImageInput.files[0];
            if (!file) {
                alert('Please select an image of your grocery receipt.');
                return;
            }

            const formData = new FormData();
            formData.append('image', file);
            formData.append('user_id', 'default');

            const submitBtn = receiptAuditorForm.querySelector('button[type="submit"]');
            const originalBtnContent = submitBtn.innerHTML;

            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Auditing...';
            submitBtn.disabled = true;
            receiptAuditResult.style.display = 'block';
            receiptAuditResult.innerHTML = '<div style="text-align: center; padding: 15px;"><i class="fas fa-spinner fa-spin"></i> Calculating your Basket Health Score...</div>';

            try {
                const res = await fetch('/audit-receipt', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (data.status === 'success') {
                    renderReceiptAuditResult(data);
                } else {
                    receiptAuditResult.innerHTML = `<div style="color: #dc2626; padding: 10px; background: #fee2e2; border-radius: 8px;">Error: ${data.message}</div>`;
                }
            } catch (err) {
                console.error("Receipt Audit Error:", err);
                receiptAuditResult.innerHTML = `<div style="color: #dc2626; padding: 10px; background: #fee2e2; border-radius: 8px;">Error: ${err.message}</div>`;
            } finally {
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
            }
        });
    }

    function renderFoodScanResult(data) {
        const gradeColor = data.grade === 'Green' ? '#10b981' : data.grade === 'Yellow' ? '#f59e0b' : '#ef4444';
        const gradeBg = data.grade === 'Green' ? '#ecfdf5' : data.grade === 'Yellow' ? '#fffbeb' : '#fef2f2';

        foodScanResult.innerHTML = `
            <div style="background: #f9fafb; border-radius: 12px; border: 1px solid #e5e7eb; overflow: hidden; margin-top: 15px;">
                <div style="background: ${gradeBg}; padding: 12px; border-bottom: 2px solid ${gradeColor}; display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #374151; font-size: 0.9rem;">Safety Grade</h4>
                    <span style="background: ${gradeColor}; color: white; padding: 2px 10px; border-radius: 20px; font-weight: 700; font-size: 0.8rem;">${data.grade}</span>
                </div>
                <div style="padding: 15px;">
                    <p style="font-size: 0.85rem; margin-bottom: 15px; font-weight: 500;">${data.summary || 'Scan complete.'}</p>
                    
                    ${data.risks && data.risks.length > 0 ? `
                        <div style="margin-bottom: 12px;">
                            <h5 style="font-size: 0.75rem; color: #ef4444; text-transform: uppercase;">Personal Risks</h5>
                            <ul style="padding-left: 15px; font-size: 0.8rem; color: #4b5563;">
                                ${data.risks.map(risk => `<li>${risk}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${data.alternatives && data.alternatives.length > 0 ? `
                        <div>
                            <h5 style="font-size: 0.75rem; color: #10b981; text-transform: uppercase;">Try These Instead</h5>
                            <ul style="padding-left: 15px; font-size: 0.8rem; color: #4b5563;">
                                ${data.alternatives.map(alt => `<li>${alt}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    function renderReceiptAuditResult(data) {
        const scoreColor = data.health_score >= 80 ? '#10b981' : data.health_score >= 60 ? '#f59e0b' : '#ef4444';
        
        receiptAuditResult.innerHTML = `
            <div style="background: #f9fafb; border-radius: 12px; border: 1px solid #e5e7eb; overflow: hidden; margin-top: 15px;">
                <div style="padding: 15px; text-align: center; border-bottom: 1px solid #e5e7eb;">
                    <h5 style="margin: 0 0 10px 0; color: #6b7280; font-size: 0.8rem; text-transform: uppercase;">Basket Health Score</h5>
                    <div style="font-size: 2.5rem; font-weight: 800; color: ${scoreColor};">${data.health_score}/100</div>
                    <p style="font-size: 0.8rem; color: #4b5563; margin-top: 10px;">${data.personalized_advice || ''}</p>
                </div>
                <div style="padding: 15px;">
                    ${data.red_flags && data.red_flags.length > 0 ? `
                        <div style="margin-bottom: 12px;">
                            <h5 style="font-size: 0.75rem; color: #ef4444; text-transform: uppercase;">Red Flags Found</h5>
                            <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-top: 5px;">
                                ${data.red_flags.map(flag => `<span style="background: #fee2e2; color: #dc2626; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">${flag}</span>`).join('')}
                            </div>
                        </div>
                    ` : ''}

                    ${data.swaps && data.swaps.length > 0 ? `
                        <div>
                            <h5 style="font-size: 0.75rem; color: #10b981; text-transform: uppercase;">Suggested Health Swaps</h5>
                            <ul style="padding-left: 15px; font-size: 0.8rem; color: #4b5563; margin-top: 5px;">
                                ${data.swaps.map(swap => `<li>${swap}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    // Insurance Modal Functions
    insuranceBtn.addEventListener('click', (e) => {
        e.preventDefault();
        insuranceModal.classList.add('show');
    });

    closeInsuranceBtn.addEventListener('click', () => {
        insuranceModal.classList.remove('show');
    });

    insuranceModal.addEventListener('click', (e) => {
        if (e.target === insuranceModal) insuranceModal.classList.remove('show');
    });

    // First Aid Modal Functions
    first_aid_btn_listener = (e) => {
        e.preventDefault();
        firstAidModal.classList.add('show');
    };
    if (firstAidBtn) firstAidBtn.addEventListener('click', first_aid_btn_listener);

    if (closeFirstAidBtn) closeFirstAidBtn.addEventListener('click', () => {
        firstAidModal.classList.remove('show');
    });

    firstAidModal.addEventListener('click', (e) => {
        if (e.target === firstAidModal) firstAidModal.classList.remove('show');
    });

    // Symptom Cam Modal Functions
    if (symptomCamBtn) symptomCamBtn.addEventListener('click', (e) => {
        e.preventDefault();
        symptomCamModal.classList.add('show');
    });

    if (closeSymptomCamBtn) closeSymptomCamBtn.addEventListener('click', () => {
        symptomCamModal.classList.remove('show');
    });

    if (symptomCamModal) symptomCamModal.addEventListener('click', (e) => {
        if (e.target === symptomCamModal) symptomCamModal.classList.remove('show');
    });

    // Symptom Cam File Preview
    if (symptomImageInput) {
        symptomImageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    symptomPreviewImage.src = e.target.result;
                    symptomFilePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                symptomFilePreview.style.display = 'none';
            }
        });
    }

    // Symptom Cam Form Submission
    if (symptomCamForm) {
        symptomCamForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const file = symptomImageInput.files[0];
            const context = symptomContext.value.trim();

            if (!file) {
                alert('Please select an image of the symptom.');
                return;
            }

            const formData = new FormData();
            formData.append('image', file);
            formData.append('symptoms_history', context);
            formData.append('user_id', 'default');

            const submitBtn = symptomCamForm.querySelector('button[type="submit"]');
            const originalBtnContent = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            submitBtn.disabled = true;
            symptomCamResult.style.display = 'block';
            symptomCamResult.innerHTML = '<div style="text-align: center; padding: 20px;"><i class="fas fa-spinner fa-spin"></i> Our medical AI is analyzing your image. This may take a few seconds...</div>';

            try {
                const res = await fetch('/symptom-cam', {
                    method: 'POST',
                    body: formData
                });

                if (!res.ok) throw new Error(`Server error: ${res.status}`);
                const data = await res.json();

                if (data.status === 'success') {
                    renderSymptomCamResult(data);
                } else {
                    symptomCamResult.innerHTML = `<div class="error-message" style="color: #dc2626; padding: 15px; background: #fee2e2; border-radius: 8px;">
                        <i class="fas fa-exclamation-circle"></i> ${data.message || 'Analysis failed. Please try describing your symptoms in the chat instead.'}
                    </div>`;
                }
            } catch (err) {
                console.error("Symptom Cam Error:", err);
                symptomCamResult.innerHTML = `<div class="error-message" style="color: #dc2626; padding: 15px; background: #fee2e2; border-radius: 8px;">
                    <i class="fas fa-times-circle"></i> Error: ${err.message}. Please check your connection and try again.
                </div>`;
            } finally {
                submitBtn.innerHTML = originalBtnContent;
                submitBtn.disabled = false;
            }
        });
    }

    function renderSymptomCamResult(data) {
        const urgencyClass = data.urgency ? data.urgency.toLowerCase() : 'routine';
        const urgencyIcon = urgencyClass === 'emergency' ? 'alert-triangle' : 
                          urgencyClass === 'urgent' ? 'exclamation-circle' : 'info-circle';
        
        symptomCamResult.innerHTML = `
            <div class="analysis-card" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; margin-top: 20px;">
                <div class="analysis-header" style="background: #ffffff; padding: 15px; border-bottom: 2px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #1e293b;"><i class="fas fa-microscope" style="color: var(--primary-color);"></i> Visual Analysis Result</h4>
                    <span class="urgency-badge ${urgencyClass}" style="padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">
                        <i class="fas fa-${urgencyIcon}"></i> ${data.urgency}
                    </span>
                </div>
                <div class="analysis-body" style="padding: 20px;">
                    <p style="margin-bottom: 20px; font-size: 0.95rem; line-height: 1.6; color: #334155;">${data.analysis}</p>
                    
                    ${data.possible_indications && data.possible_indications.length > 0 ? `
                        <div style="margin-bottom: 20px;">
                            <h5 style="margin-bottom: 10px; color: #475569; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Possible Indications</h5>
                            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                                ${data.possible_indications.map(ind => `<span style="background: #eef2ff; color: #4f46e5; padding: 4px 12px; border-radius: 15px; font-size: 0.85rem; border: 1px solid #c7d2fe;">${ind}</span>`).join('')}
                            </div>
                        </div>
                    ` : ''}

                    <div style="background: #fff; border-left: 4px solid var(--primary-color); padding: 15px; border-radius: 0 8px 8px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <h5 style="margin-bottom: 5px; color: var(--primary-color); font-size: 0.85rem; text-transform: uppercase;">Actionable Recommendation</h5>
                        <p style="margin: 0; font-weight: 500; font-size: 0.95rem; color: #1e293b;">${data.recommendation}</p>
                    </div>

                    <div style="margin-top: 20px; font-size: 0.75rem; color: #94a3b8; font-style: italic; text-align: center;">
                        <i class="fas fa-info-circle"></i> DISCLAIMER: This is an AI-powered assessment for educational purposes and not a professional medical diagnosis. Please consult a healthcare professional for clinical evaluation.
                    </div>
                </div>
            </div>
        `;
    }

    // Pharmacy Locator Functions
    pharmacyBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openPharmacyLocator();
    });

    closePharmacyBtn.addEventListener('click', () => {
        pharmacyModal.classList.remove('show');
    });

    pharmacyModal.addEventListener('click', (e) => {
        if (e.target === pharmacyModal) {
            pharmacyModal.classList.remove('show');
        }
    });

    async function openPharmacyLocator() {
        pharmacyModal.classList.add('show');

        // Get user's location
        if (navigator.geolocation) {
            const locationStatus = document.querySelector('.location-status-pharmacy');
            locationStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting your location...';
            locationStatus.style.display = 'block';

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    locationStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Finding nearby 24/7 pharmacies...';

                    try {
                        const response = await fetch(`/nearby-pharmacies?lat=${lat}&lon=${lon}&max_results=5`);
                        const data = await response.json();

                        if (data.pharmacies && data.pharmacies.length > 0) {
                            displayPharmacies(data.pharmacies);
                            locationStatus.style.display = 'none';
                        } else {
                            locationStatus.innerHTML = '<i class="fas fa-info-circle"></i> No 24/7 pharmacies found nearby. Try expanding your search radius.';
                        }
                    } catch (error) {
                        console.error('Error fetching pharmacies:', error);
                        locationStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Error loading pharmacies. Please try again.';
                    }
                },
                (error) => {
                    console.error('Geolocation error:', error);
                    locationStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Unable to get your location. Please enable location services.';
                }
            );
        } else {
            const locationStatus = document.querySelector('.location-status-pharmacy');
            locationStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Geolocation is not supported by your browser.';
        }
    }

    function displayPharmacies(pharmacies) {
        pharmaciesList.innerHTML = '';

        pharmacies.forEach(pharmacy => {
            const pharmacyItem = document.createElement('div');
            pharmacyItem.className = 'hospital-item'; // Reusing hospital item styles

            pharmacyItem.innerHTML = `
                <div class="hospital-name">
                    <i class="fas fa-prescription-bottle-alt"></i>
                    ${pharmacy.name}
                    <span class="hospital-distance">${pharmacy.distance_km} km</span>
                    <span class="hospital-type private">24/7</span>
                </div>
                <div class="hospital-details">
                    <div class="hospital-detail">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>${pharmacy.address}</span>
                    </div>
                    <div class="hospital-detail">
                        <i class="fas fa-phone"></i>
                        <a href="tel:${pharmacy.phone}" style="color: inherit; text-decoration: none;">${pharmacy.phone}</a>
                    </div>
                </div>
            `;

            pharmaciesList.appendChild(pharmacyItem);
        });
    }

    async function openHospitalLocator() {
        hospitalModal.classList.add('show');

        // Get user's location
        if (navigator.geolocation) {
            const locationStatus = document.querySelector('.location-status');
            locationStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting your location...';

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    locationStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Finding nearby hospitals...';

                    try {
                        const response = await fetch(`/nearby-hospitals?lat=${lat}&lon=${lon}&max_results=5`);
                        const data = await response.json();

                        if (data.hospitals && data.hospitals.length > 0) {
                            displayHospitals(data.hospitals);
                            locationStatus.style.display = 'none';
                        } else {
                            locationStatus.innerHTML = '<i class="fas fa-info-circle"></i> No hospitals found nearby. Try expanding your search radius.';
                        }
                    } catch (error) {
                        console.error('Error fetching hospitals:', error);
                        locationStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Error loading hospitals. Please try again.';
                    }
                },
                (error) => {
                    console.error('Geolocation error:', error);
                    locationStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Unable to get your location. Please enable location services.';
                }
            );
        } else {
            const locationStatus = document.querySelector('.location-status');
            locationStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Geolocation is not supported by your browser.';
        }
    }

    function displayHospitals(hospitals) {
        hospitalsList.innerHTML = '';

        hospitals.forEach(hospital => {
            const hospitalItem = document.createElement('div');
            hospitalItem.className = 'hospital-item';

            const typeClass = hospital.type.toLowerCase();

            hospitalItem.innerHTML = `
                <div class="hospital-name">
                    <i class="fas fa-hospital"></i>
                    ${hospital.name}
                    <span class="hospital-distance">${hospital.distance_km} km</span>
                    <span class="hospital-type ${typeClass}">${hospital.type}</span>
                </div>
                <div class="hospital-details">
                    <div class="hospital-detail">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>${hospital.address}</span>
                    </div>
                    <div class="hospital-detail">
                        <i class="fas fa-phone"></i>
                        <a href="tel:${hospital.phone}" style="color: inherit; text-decoration: none;">${hospital.phone}</a>
                    </div>
                    ${hospital.emergency ? '<div class="hospital-detail"><i class="fas fa-ambulance"></i><span>24/7 Emergency Services</span></div>' : ''}
                </div>
            `;

            hospitalsList.appendChild(hospitalItem);
        });
    }

    // Wellness Modal Functions
    wellnessBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await loadWellnessData();
        wellnessModal.classList.add('show');
    });

    closeWellnessBtn.addEventListener('click', () => {
        wellnessModal.classList.remove('show');
    });

    wellnessModal.addEventListener('click', (e) => {
        if (e.target === wellnessModal) {
            wellnessModal.classList.remove('show');
        }
    });

    async function loadWellnessData() {
        try {
            // Load daily tip
            const dailyTipResponse = await fetch('/daily-tip?user_id=default');
            const dailyTipData = await dailyTipResponse.json();
            document.getElementById('daily-tip').textContent = dailyTipData.tip;

            // Load wellness tips
            const tipsResponse = await fetch('/wellness-tips?user_id=default&count=5');
            const tipsData = await tipsResponse.json();

            const tipsList = document.getElementById('wellness-tips-list');
            if (tipsData.tips && tipsData.tips.length > 0) {
                tipsList.innerHTML = '';
                tipsData.tips.forEach(tip => {
                    const tipItem = document.createElement('div');
                    tipItem.className = 'wellness-tip-item';
                    tipItem.textContent = tip;
                    tipsList.appendChild(tipItem);
                });
            } else {
                tipsList.innerHTML = '<p class="no-data">No tips available</p>';
            }

            // Load proactive alerts
            const alertsResponse = await fetch('/proactive-alerts?user_id=default');
            const alertsData = await alertsResponse.json();

            const alertsList = document.getElementById('proactive-alerts-list');
            if (alertsData.alerts && alertsData.alerts.length > 0) {
                alertsList.innerHTML = '';
                alertsData.alerts.forEach(alert => {
                    const alertItem = document.createElement('div');
                    alertItem.className = `alert-item priority-${alert.priority}`;
                    alertItem.innerHTML = `
                        <div class="alert-content">
                            <div class="alert-message">${alert.message}</div>
                            <div class="alert-action">${alert.action}</div>
                        </div>
                    `;
                    alertsList.appendChild(alertItem);
                });
            } else {
                alertsList.innerHTML = '<p class="no-data">No alerts at this time</p>';
            }
        } catch (error) {
            console.error('Error loading wellness data:', error);
        }
    }

    // Prescriptions Modal Functions
    prescriptionsBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await loadPrescriptions();
        prescriptionsModal.classList.add('show');
    });

    closePrescriptionsBtn.addEventListener('click', () => {
        prescriptionsModal.classList.remove('show');
    });

    prescriptionsModal.addEventListener('click', (e) => {
        if (e.target === prescriptionsModal) {
            prescriptionsModal.classList.remove('show');
        }
    });

    // File preview
    prescriptionFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                filePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Upload prescription
    prescriptionUploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = prescriptionFileInput.files[0];
        if (!file) {
            alert('Please select a file');
            return;
        }

        const formData = new FormData();
        formData.append('prescription', file);
        formData.append('user_id', 'default');

        const uploadBtn = document.getElementById('upload-btn');
        const originalText = uploadBtn.innerHTML;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        uploadBtn.disabled = true;

        try {
            const response = await fetch('/upload-prescription', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                alert('Prescription uploaded successfully!');
                prescriptionUploadForm.reset();
                filePreview.style.display = 'none';
                await loadPrescriptions();
            } else {
                alert('Error: ' + (data.error || 'Upload failed'));
            }
        } catch (error) {
            console.error('Error uploading prescription:', error);
            alert('Error uploading prescription. Please try again.');
        } finally {
            uploadBtn.innerHTML = originalText;
            uploadBtn.disabled = false;
        }
    });

    async function loadPrescriptions() {
        try {
            const response = await fetch('/prescriptions?user_id=default');
            const data = await response.json();

            if (data.prescriptions && data.prescriptions.length > 0) {
                displayPrescriptions(data.prescriptions);
            } else {
                prescriptionsList.innerHTML = '<p class="no-data">No prescriptions uploaded yet</p>';
            }
        } catch (error) {
            console.error('Error loading prescriptions:', error);
            prescriptionsList.innerHTML = '<p class="no-data">Error loading prescriptions</p>';
        }
    }

    function displayPrescriptions(prescriptions) {
        prescriptionsList.innerHTML = '';

        prescriptions.forEach(prescription => {
            const prescriptionCard = document.createElement('div');
            prescriptionCard.className = 'prescription-card';

            const medications = prescription.medications && prescription.medications.length > 0
                ? prescription.medications.slice(0, 3).join(', ')
                : 'No medications detected';

            prescriptionCard.innerHTML = `
                <div class="prescription-header">
                    <div class="prescription-info">
                        <i class="fas fa-file-prescription"></i>
                        <div>
                            <strong>${prescription.filename}</strong>
                            <small>${new Date(prescription.upload_date).toLocaleDateString()}</small>
                        </div>
                    </div>
                    <button class="delete-prescription-btn" data-id="${prescription.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="prescription-details">
                    ${prescription.doctor_name ? `<p><strong>Doctor:</strong> ${prescription.doctor_name}</p>` : ''}
                    ${prescription.date ? `<p><strong>Date:</strong> ${prescription.date}</p>` : ''}
                    <p><strong>Medications:</strong> ${medications}</p>
                </div>
                <details class="prescription-text-details">
                    <summary>View Extracted Text</summary>
                    <pre>${prescription.extracted_text || 'No text extracted'}</pre>
                </details>
            `;

            prescriptionsList.appendChild(prescriptionCard);
        });

        // Add delete handlers
        document.querySelectorAll('.delete-prescription-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const prescriptionId = e.currentTarget.getAttribute('data-id');
                if (confirm('Are you sure you want to delete this prescription?')) {
                    await deletePrescription(prescriptionId);
                }
            });
        });
    }

    async function deletePrescription(prescriptionId) {
        try {
            const response = await fetch(`/prescription/${prescriptionId}?user_id=default`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (data.success) {
                await loadPrescriptions();
            } else {
                alert('Error deleting prescription');
            }
        } catch (error) {
            console.error('Error deleting prescription:', error);
            alert('Error deleting prescription');
        }
    }

    // Lab Tests Modal Functionality
    labTestsBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await loadLabReports();
        labTestsModal.classList.add('show');
    });

    closeLabTestsBtn.addEventListener('click', () => {
        labTestsModal.classList.remove('show');
    });

    labTestsModal.addEventListener('click', (e) => {
        if (e.target === labTestsModal) {
            labTestsModal.classList.remove('show');
        }
    });

    // File preview for lab reports
    labReportFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                labPreviewImage.src = e.target.result;
                labFilePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Upload lab report
    labReportUploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = labReportFileInput.files[0];
        if (!file) {
            alert('Please select a file');
            return;
        }

        const formData = new FormData();
        formData.append('lab_report', file);
        formData.append('user_id', 'default');

        const uploadBtn = document.getElementById('upload-lab-btn');
        const originalText = uploadBtn.innerHTML;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        uploadBtn.disabled = true;

        try {
            const response = await fetch('/upload-lab-report', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                alert('Lab report uploaded and analyzed successfully!');
                labReportUploadForm.reset();
                labFilePreview.style.display = 'none';

                // Reload reports list
                await loadLabReports();

                // Display analysis
                displayLabAnalysis(data.lab_report);
            } else {
                alert('Error: ' + (data.error || 'Upload failed'));
            }
        } catch (error) {
            console.error('Error uploading lab report:', error);
            alert('Error uploading lab report. Please try again.');
        } finally {
            uploadBtn.innerHTML = originalText;
            uploadBtn.disabled = false;
        }
    });

    // Load lab reports
    async function loadLabReports() {
        try {
            const response = await fetch('/lab-reports?user_id=default');
            const data = await response.json();

            if (data.lab_reports && data.lab_reports.length > 0) {
                displayLabReports(data.lab_reports);
            } else {
                labReportsList.innerHTML = '<p class="no-data">No lab reports uploaded yet</p>';
            }
        } catch (error) {
            console.error('Error loading lab reports:', error);
            labReportsList.innerHTML = '<p class="no-data">Error loading lab reports</p>';
        }
    }

    // Display lab reports list
    function displayLabReports(reports) {
        labReportsList.innerHTML = '';

        reports.forEach(report => {
            const reportCard = document.createElement('div');
            reportCard.className = 'lab-report-card';

            const statusClass = getStatusClass(report.overall_status);
            const date = new Date(report.upload_date).toLocaleDateString();

            reportCard.innerHTML = `
                <div class="lab-report-header">
                    <div>
                        <div class="lab-report-title">${report.filename}</div>
                        <div class="lab-report-date">${date}</div>
                    </div>
                    <button class="delete-lab-report-btn" data-id="${report.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="lab-report-category">${report.test_category}</div>
                <span class="lab-report-status ${statusClass}">${report.overall_status}</span>
            `;

            // View report on click
            reportCard.addEventListener('click', async (e) => {
                if (!e.target.closest('.delete-lab-report-btn')) {
                    await viewLabReport(report.id);
                }
            });

            // Delete button
            const deleteBtn = reportCard.querySelector('.delete-lab-report-btn');
            deleteBtn.addEventListener('click', async (e) => {
                e.stopPropagation();
                if (confirm('Are you sure you want to delete this lab report?')) {
                    await deleteLabReport(report.id);
                }
            });

            labReportsList.appendChild(reportCard);
        });
    }

    // Get status class for color coding
    function getStatusClass(status) {
        if (!status) return 'normal';
        const statusLower = status.toLowerCase();
        if (statusLower.includes('critical') || statusLower.includes('immediate')) {
            return 'critical';
        } else if (statusLower.includes('abnormal') || statusLower.includes('attention') || statusLower.includes('need')) {
            return 'attention';
        } else {
            return 'normal';
        }
    }

    // View lab report details
    async function viewLabReport(reportId) {
        try {
            const response = await fetch(`/lab-report/${reportId}?user_id=default`);
            const data = await response.json();

            if (data.lab_report) {
                displayLabAnalysis(data.lab_report);
            }
        } catch (error) {
            console.error('Error viewing lab report:', error);
            alert('Error loading lab report details');
        }
    }

    // Display lab analysis
    function displayLabAnalysis(labReport) {
        currentLabReportId = labReport.id;
        const analysis = labReport.analysis;

        // Show analysis section
        labAnalysisSection.style.display = 'block';

        // Set test category
        document.getElementById('analysis-test-category').textContent = labReport.test_category;

        // Set overall status
        const statusClass = getStatusClass(analysis.overall_status);
        const statusIcon = document.getElementById('overall-status-icon');
        statusIcon.className = `status-icon ${statusClass}`;

        if (statusClass === 'normal') {
            statusIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        } else if (statusClass === 'attention') {
            statusIcon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
        } else {
            statusIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        }

        document.getElementById('overall-status-text').textContent = analysis.overall_status;

        // Set summary
        document.getElementById('analysis-summary-text').textContent = analysis.summary || 'Analysis complete.';

        // Display parameters
        displayParameters(analysis.parameters || []);

        // Display recommendations
        displayRecommendations(analysis.lifestyle_recommendations || []);

        // Display doctor consultation advice
        displayDoctorConsultation(analysis.when_to_consult_doctor || []);

        // Reset chat
        labChatMessages.innerHTML = `
            <div class="message bot">
                <div class="bubble">
                    I can help you understand your ${labReport.test_category} results. Feel free to ask any questions!
                </div>
            </div>
        `;

        // Scroll to analysis
        labAnalysisSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Display parameters
    function displayParameters(parameters) {
        const parametersList = document.getElementById('parameters-list');
        parametersList.innerHTML = '';

        parameters.forEach(param => {
            const paramCard = document.createElement('div');
            paramCard.className = `parameter-card ${param.status}`;

            const statusIcon = param.status === 'normal' ? '✓' :
                param.status === 'low' ? '↓' :
                    param.status === 'high' ? '↑' : '?';

            const hasRecommendations = param.recommendations && param.recommendations.length > 0;

            paramCard.innerHTML = `
                <div class="parameter-header">
                    <span class="parameter-name">${param.name}</span>
                    <span class="parameter-status ${param.status}">
                        ${statusIcon} ${param.status.toUpperCase()}
                    </span>
                </div>
                <div class="parameter-value">
                    <span class="value-display">${param.value} ${param.unit}</span>
                    <span class="normal-range">Normal: ${param.normal_range}</span>
                </div>
                <div class="parameter-interpretation">${param.interpretation}</div>
                ${hasRecommendations ? `
                    <details class="parameter-recommendations">
                        <summary>View Recommendations</summary>
                        <ul>
                            ${param.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </details>
                ` : ''}
            `;

            parametersList.appendChild(paramCard);
        });
    }

    // Display recommendations
    function displayRecommendations(recommendations) {
        const recommendationsList = document.getElementById('lifestyle-recommendations');

        if (recommendations.length > 0) {
            recommendationsList.innerHTML = recommendations.map(rec => `<li>${rec}</li>`).join('');
            document.querySelector('.recommendations-section').style.display = 'block';
        } else {
            document.querySelector('.recommendations-section').style.display = 'none';
        }
    }

    // Display doctor consultation advice
    function displayDoctorConsultation(consultationAdvice) {
        const consultationList = document.getElementById('doctor-consultation-list');

        if (consultationAdvice.length > 0) {
            consultationList.innerHTML = consultationAdvice.map(advice => `<li>${advice}</li>`).join('');
            document.querySelector('.doctor-consultation-section').style.display = 'block';
        } else {
            document.querySelector('.doctor-consultation-section').style.display = 'none';
        }
    }

    // Close analysis section
    closeAnalysisBtn.addEventListener('click', () => {
        labAnalysisSection.style.display = 'none';
        currentLabReportId = null;
    });

    // Delete lab report
    async function deleteLabReport(reportId) {
        try {
            const response = await fetch(`/lab-report/${reportId}?user_id=default`, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (data.success) {
                alert('Lab report deleted successfully');
                await loadLabReports();

                // Hide analysis if viewing deleted report
                if (currentLabReportId === reportId) {
                    labAnalysisSection.style.display = 'none';
                    currentLabReportId = null;
                }
            } else {
                alert('Error deleting lab report');
            }
        } catch (error) {
            console.error('Error deleting lab report:', error);
            alert('Error deleting lab report');
        }
    }

    // Lab test chat
    labChatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = labChatInput.value.trim();
        if (!message) return;

        // Add user message
        addLabChatMessage(message, 'user');
        labChatInput.value = '';

        try {
            const response = await fetch('/lab-test-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    user_id: 'default',
                    report_id: currentLabReportId,
                    language: currentLanguage
                })
            });

            const data = await response.json();

            if (data.response) {
                addLabChatMessage(data.response, 'bot');
            } else if (data.error) {
                addLabChatMessage('Error: ' + data.error, 'bot');
            }
        } catch (error) {
            console.error('Error in lab chat:', error);
            addLabChatMessage('Sorry, something went wrong. Please try again.', 'bot');
        }
    });

    function addLabChatMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');
        bubbleDiv.textContent = text;

        messageDiv.appendChild(bubbleDiv);
        labChatMessages.appendChild(messageDiv);

        // Scroll to bottom
        labChatMessages.scrollTop = labChatMessages.scrollHeight;
    }

    // Challenges Modal Functionality
    const challengesBtn = document.getElementById('challenges-btn');
    const challengesModal = document.getElementById('challenges-modal');
    const closeChallengesBtn = document.querySelector('.close-challenges');

    challengesBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await loadChallenges();
        challengesModal.classList.add('show');
    });

    closeChallengesBtn.addEventListener('click', () => {
        challengesModal.classList.remove('show');
    });

    challengesModal.addEventListener('click', (e) => {
        if (e.target === challengesModal) {
            challengesModal.classList.remove('show');
        }
    });

    // Tab Switching
    const challengeTabs = challengesModal.querySelectorAll('.tab-btn');
    const challengeContents = challengesModal.querySelectorAll('.tab-content');

    challengeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            challengeTabs.forEach(t => t.classList.remove('active'));
            challengeContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Load Challenges
    async function loadChallenges() {
        try {
            const response = await fetch('/challenges?user_id=default');
            const data = await response.json();

            if (data.challenges) {
                displayChallenges(data.challenges, data.user_stats);
            }
        } catch (error) {
            console.error('Error loading challenges:', error);
        }
    }

    // Display Challenges
    function displayChallenges(challenges, userStats) {
        // Update stats
        totalPointsEl.textContent = userStats.points;
        totalBadgesEl.textContent = userStats.badges.length;

        const activeList = document.getElementById('active-challenges-list');
        const availableList = document.getElementById('available-challenges-list');
        const completedList = document.getElementById('completed-challenges-list');

        activeList.innerHTML = '';
        availableList.innerHTML = '';
        completedList.innerHTML = '';

        challenges.forEach(challenge => {
            const card = createChallengeCard(challenge);

            if (challenge.status === 'active') {
                activeList.appendChild(card);
            } else if (challenge.status === 'completed') {
                completedList.appendChild(card);
            } else {
                availableList.appendChild(card);
            }
        });

        // Show empty states if needed
        if (activeList.children.length === 0) {
            activeList.innerHTML = '<p class="no-data">No active challenges. Join one to get started!</p>';
        }
        if (availableList.children.length === 0) {
            availableList.innerHTML = '<p class="no-data">No new challenges available right now.</p>';
        }
        if (completedList.children.length === 0) {
            completedList.innerHTML = '<p class="no-data">Complete challenges to see them here.</p>';
        }

        // Load leaderboard
        loadLeaderboard(userStats.points);
    }

    // Create Challenge Card
    function createChallengeCard(challenge) {
        const card = document.createElement('div');
        card.className = 'challenge-card';

        let actionButton = '';
        let progressSection = '';
        let statusBadge = '';

        if (challenge.status === 'active') {
            const progress = challenge.progress;
            const percent = (progress.days_completed / challenge.duration_days) * 100;

            // Check if logged today
            const today = new Date().toISOString().split('T')[0];
            const loggedToday = progress.last_log_date === today;

            progressSection = `
                <div class="progress-ring" style="--progress: ${percent * 3.6}deg">
                    <div class="ring-container">
                        <div class="ring-inner">
                            ${Math.round(percent)}%
                        </div>
                    </div>
                    <div class="progress-details">
                        <span class="progress-label">Progress</span>
                        <span class="progress-value">${progress.days_completed} / ${challenge.duration_days} Days</span>
                    </div>
                </div>
            `;

            actionButton = `
                <button class="card-btn ${loggedToday ? 'btn-disabled' : 'btn-success'}" 
                        onclick="logChallengeProgress('${challenge.id}')" 
                        ${loggedToday ? 'disabled' : ''}>
                    ${loggedToday ? '<i class="fas fa-check-circle"></i> Logged Today' : '<i class="fas fa-edit"></i> Log Progress'}
                </button>
            `;
        } else if (challenge.status === 'available') {
            actionButton = `
                <button class="card-btn btn-primary" onclick="joinChallenge('${challenge.id}')">
                    <i class="fas fa-plus-circle"></i> Join Challenge
                </button>
            `;
        } else if (challenge.status === 'completed') {
            statusBadge = `<span class="card-badge">Completed</span>`;
            progressSection = `
                <div class="progress-ring" style="--progress: 360deg">
                    <div class="ring-container">
                        <div class="ring-inner">
                            <i class="fas fa-check" style="color: var(--primary-color)"></i>
                        </div>
                    </div>
                    <div class="progress-details">
                        <span class="progress-label">Status</span>
                        <span class="progress-value">Challenge Complete!</span>
                    </div>
                </div>
            `;
        }

        card.innerHTML = `
            <div class="card-header">
                <div class="card-icon">${challenge.icon}</div>
                ${statusBadge}
            </div>
            <h3 class="card-title">${challenge.name}</h3>
            <div class="card-desc">${challenge.description}</div>
            
            ${progressSection}
            
            ${actionButton ? actionButton : ''}
        `;

        return card;
    }

    // Expose functions to global scope for onclick handlers
    window.joinChallenge = async (challengeId) => {
        try {
            const response = await fetch('/challenges/join', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: 'default',
                    challenge_id: challengeId
                })
            });

            const data = await response.json();
            if (data.success) {
                alert('Challenge joined successfully!');
                await loadChallenges();
                // Switch to active tab
                document.querySelector('[data-tab="active-challenges"]').click();
            } else {
                alert(data.error || 'Failed to join challenge');
            }
        } catch (error) {
            console.error('Error joining challenge:', error);
            alert('Error joining challenge');
        }
    };

    window.logChallengeProgress = async (challengeId) => {
        try {
            const response = await fetch('/challenges/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: 'default',
                    challenge_id: challengeId
                })
            });

            const data = await response.json();
            if (data.success) {
                let msg = `Progress logged! +${data.points_earned} points.`;
                if (data.completed) {
                    msg += `\n🎉 Challenge Completed! +${data.bonus_points} bonus points!\nYou earned the "${data.badge.name}" badge!`;
                }
                alert(msg);
                await loadChallenges();
            } else {
                alert(data.error || 'Failed to log progress');
            }
        } catch (error) {
            console.error('Error logging progress:', error);
            alert('Error logging progress');
        }
    };

    // Leaderboard Logic
    function loadLeaderboard(userPoints) {
        const leaderboardList = document.getElementById('leaderboard-list');
        leaderboardList.innerHTML = '';

        // Mock Data with dynamic points based on user to keep it competitive
        const leaderboardData = [
            { name: "Sarah K.", points: Math.max(320, userPoints + 50), avatar: "S" },
            { name: "Mike R.", points: Math.max(280, userPoints + 20), avatar: "M" },
            { name: "Priya D.", points: Math.max(210, userPoints - 10), avatar: "P" },
            { name: "You", points: userPoints, avatar: "U", isUser: true },
            { name: "John D.", points: Math.max(120, userPoints - 80), avatar: "J" },
            { name: "Emma W.", points: Math.max(90, userPoints - 100), avatar: "E" }
        ];

        // Sort by points
        leaderboardData.sort((a, b) => b.points - a.points);

        leaderboardData.forEach((user, index) => {
            const rank = index + 1;
            const isTop3 = rank <= 3;
            const rankClass = isTop3 ? `top-${rank}` : '';
            const userClass = user.isUser ? 'current-user' : '';

            const item = document.createElement('div');
            item.className = `leaderboard-item ${userClass}`;
            item.innerHTML = `
                <div class="rank ${rankClass}">${rank}</div>
                <div class="user-info-cell">
                    <div class="user-avatar">${user.avatar}</div>
                    <span class="user-name">${user.name}</span>
                    ${user.isUser ? '<span style="font-size: 0.7em; background: var(--primary-color); color: white; padding: 2px 8px; border-radius: 10px; font-weight: 700;">YOU</span>' : ''}
                </div>
                <div class="user-points">${user.points} pts</div>
            `;
            leaderboardList.appendChild(item);
        });
    }

    // --- NEW FEATURE HANDLERS ---

    // Food Scanner Handler
    if (foodScannerForm) foodScannerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('food-image');
        const file = fileInput.files[0];
        if (!file) return;
        const resultDiv = document.getElementById('food-scan-result');
        resultDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing ingredients...';

        const formData = new FormData();
        formData.append('image', file);
        formData.append('user_id', 'default');

        try {
            const res = await fetch('/scan-food', { method: 'POST', body: formData });
            const data = await res.json();
            resultDiv.innerHTML = `<div class="result-box" style="padding: 10px; background: #f9f9f9; border-radius: 5px;">${marked.parse(data.analysis || 'Analysis failed.')}</div>`;
        } catch (err) { resultDiv.innerHTML = 'Error scanning food.'; }
    });

    // Receipt Auditor Handler
    if (receiptAuditorForm) receiptAuditorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('receipt-image');
        const file = fileInput.files[0];
        if (!file) return;
        const resultDiv = document.getElementById('receipt-audit-result');
        resultDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Auditing basket...';

        const formData = new FormData();
        formData.append('image', file);
        formData.append('user_id', 'default');

        try {
            const res = await fetch('/audit-receipt', { method: 'POST', body: formData });
            const data = await res.json();
            resultDiv.innerHTML = `<div class="result-box" style="padding: 10px; background: #f9f9f9; border-radius: 5px;"><strong>Health Score: ${data.overall_health_score}/10</strong><br>${marked.parse(data.summary || '')}</div>`;
        } catch (err) { resultDiv.innerHTML = 'Error auditing receipt.'; }
    });


    // Digital Twin Modal open/close
    if (digitalTwinBtn) digitalTwinBtn.addEventListener('click', (e) => {
        e.preventDefault();
        digitalTwinModal.classList.add('show');
    });

    if (closeDigitalTwinBtn) closeDigitalTwinBtn.addEventListener('click', () => {
        digitalTwinModal.classList.remove('show');
    });

    if (digitalTwinModal) digitalTwinModal.addEventListener('click', (e) => {
        if (e.target === digitalTwinModal) digitalTwinModal.classList.remove('show');
    });

    // Sim chips — populate the input field
    document.querySelectorAll('.sim-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const scenarioInput = document.getElementById('simulation-scenario');
            if (scenarioInput) scenarioInput.value = chip.dataset.scenario;
        });
    });

    // Digital Twin Handler
    const runSimBtn = document.getElementById('run-simulation-btn');
    if (runSimBtn) runSimBtn.addEventListener('click', async () => {
        const scenarioInput = document.getElementById('simulation-scenario');
        const scenario = scenarioInput.value.trim();
        if (!scenario) {
            scenarioInput.focus();
            return;
        }

        const resultDiv    = document.getElementById('simulation-result');
        const modalContent = document.querySelector('#digital-twin-modal .modal-content');
        const originalHtml = runSimBtn.innerHTML;

        // Show loading
        runSimBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Simulating...';
        runSimBtn.disabled  = true;
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div style="text-align:center;padding:25px;color:#6b7280;">
                <i class="fas fa-dna fa-spin" style="font-size:2rem;color:var(--primary-color);display:block;margin-bottom:12px;"></i>
                <strong>Running your Digital Twin simulation...</strong>
                <p style="font-size:0.85rem;margin-top:6px;">Analysing lifestyle impact on your health profile</p>
            </div>`;

        // Scroll the modal's own scrollable container to the bottom
        if (modalContent) modalContent.scrollTop = modalContent.scrollHeight;

        try {
            const res  = await fetch('/simulate-health', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: 'default', scenario })
            });
            const data = await res.json();

            if (data.status === 'error' || data.status === 'fallback') {
                resultDiv.innerHTML = `<div style="color:#dc2626;padding:12px;background:#fee2e2;border-radius:8px;">
                    <i class="fas fa-exclamation-circle"></i> ${data.message || 'Simulation failed.'}</div>`;
            } else {
                renderSimulationResult(data, scenario, resultDiv);
            }
        } catch (err) {
            resultDiv.innerHTML = `<div style="color:#dc2626;padding:12px;background:#fee2e2;border-radius:8px;">
                <i class="fas fa-exclamation-circle"></i> Error: ${err.message}</div>`;
        } finally {
            runSimBtn.innerHTML = originalHtml;
            runSimBtn.disabled  = false;
            // Scroll modal container to bottom so result is visible
            if (modalContent) modalContent.scrollTop = modalContent.scrollHeight;
        }
    });

    function renderSimulationResult(data, scenario, container) {
        // Build physical changes list
        const changes = data.expected_physical_changes || [];
        const changesHtml = changes.length
            ? changes.map(c => `<li style="margin-bottom:6px;"><i class="fas fa-check-circle" style="color:#10b981;margin-right:6px;"></i>${c}</li>`).join('')
            : '<li style="color:#6b7280;">No specific changes listed.</li>';

        // Build timeline — handle both object and string formats
        const timeline = data.timeline || {};
        let timelineHtml = '';
        if (typeof timeline === 'object' && !Array.isArray(timeline)) {
            const timeKeys = ['1 week', '1 month', '6 months', '1 year'];
            // Try known keys first, then fall back to whatever keys exist
            const keys = timeKeys.filter(k => timeline[k]) .length > 0
                ? timeKeys.filter(k => timeline[k])
                : Object.keys(timeline);
            timelineHtml = keys.map(key => {
                const val = timeline[key];
                const desc = typeof val === 'object' ? Object.values(val).join(', ') : val;
                return `
                    <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:12px;">
                        <span style="min-width:80px;font-weight:700;font-size:0.78rem;color:var(--primary-color);text-transform:uppercase;padding-top:2px;">${key}</span>
                        <span style="font-size:0.88rem;color:#374151;line-height:1.5;">${desc}</span>
                    </div>`;
            }).join('');
        } else if (typeof timeline === 'string') {
            timelineHtml = `<p style="font-size:0.88rem;color:#374151;">${timeline}</p>`;
        }

        // Risk reduction
        const riskReduction = data.risk_reduction;
        let riskHtml = '';
        if (riskReduction) {
            if (typeof riskReduction === 'object') {
                riskHtml = Object.entries(riskReduction)
                    .map(([condition, pct]) => `
                        <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #f3f4f6;">
                            <span style="font-size:0.85rem;color:#374151;">${condition}</span>
                            <span style="font-weight:700;color:#10b981;font-size:0.9rem;">${pct}</span>
                        </div>`).join('');
            } else {
                riskHtml = `<p style="font-size:0.88rem;color:#374151;">${riskReduction}</p>`;
            }
        }

        container.innerHTML = `
            <div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;overflow:hidden;margin-top:16px;box-shadow:0 4px 15px rgba(0,0,0,0.06);">

                <!-- Header -->
                <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);padding:16px 20px;">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <i class="fas fa-dna" style="color:#fff;font-size:1.3rem;"></i>
                        <div>
                            <div style="color:#fff;font-weight:700;font-size:0.95rem;">Digital Twin Simulation</div>
                            <div style="color:rgba(255,255,255,0.8);font-size:0.78rem;margin-top:2px;">Scenario: ${scenario}</div>
                        </div>
                    </div>
                </div>

                <div style="padding:18px 20px;">

                    <!-- Visual preview -->
                    ${data.visual_preview_desc ? `
                    <div style="background:#f0fdf4;border-left:4px solid #10b981;padding:12px 15px;border-radius:0 8px 8px 0;margin-bottom:18px;">
                        <div style="font-size:0.75rem;font-weight:700;color:#10b981;text-transform:uppercase;margin-bottom:4px;">Health Preview</div>
                        <p style="margin:0;font-size:0.9rem;color:#1e293b;line-height:1.5;">${data.visual_preview_desc}</p>
                    </div>` : ''}

                    <!-- Physical changes -->
                    <div style="margin-bottom:18px;">
                        <h5 style="font-size:0.8rem;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;">
                            <i class="fas fa-heartbeat" style="color:#ef4444;margin-right:6px;"></i>Expected Physical Changes
                        </h5>
                        <ul style="list-style:none;padding:0;margin:0;">${changesHtml}</ul>
                    </div>

                    <!-- Timeline -->
                    ${timelineHtml ? `
                    <div style="margin-bottom:18px;">
                        <h5 style="font-size:0.8rem;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:12px;">
                            <i class="fas fa-calendar-alt" style="color:#6366f1;margin-right:6px;"></i>Timeline
                        </h5>
                        <div style="background:#f8fafc;border-radius:8px;padding:14px;">${timelineHtml}</div>
                    </div>` : ''}

                    <!-- Risk reduction -->
                    ${riskHtml ? `
                    <div>
                        <h5 style="font-size:0.8rem;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;">
                            <i class="fas fa-shield-alt" style="color:#f59e0b;margin-right:6px;"></i>Risk Reduction
                        </h5>
                        <div style="background:#fffbeb;border-radius:8px;padding:10px 14px;">${riskHtml}</div>
                    </div>` : ''}

                </div>

                <!-- Disclaimer -->
                <div style="padding:10px 20px;background:#f9fafb;border-top:1px solid #f3f4f6;font-size:0.72rem;color:#9ca3af;text-align:center;">
                    <i class="fas fa-info-circle"></i> AI-generated prediction for educational purposes. Consult a doctor before making health decisions.
                </div>
            </div>`;
    }

    // Lab Trends Handler
    if (viewLabTrendsBtn) viewLabTrendsBtn.addEventListener('click', async () => {
        if (labTrendsSection) labTrendsSection.style.display = 'block';
        const trendsContent = document.getElementById('trends-content');
        if (trendsContent) trendsContent.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Fetching trends...';

        try {
            const res = await fetch('/lab-trends?user_id=default');
            const data = await res.json();
            if (trendsContent) trendsContent.innerHTML = marked.parse(data.summary || 'No trends found.');
        } catch (err) { if (trendsContent) trendsContent.innerHTML = 'Error fetching trends.'; }
    });

    if (closeTrendsBtn) closeTrendsBtn.addEventListener('click', () => {
        if (labTrendsSection) labTrendsSection.style.display = 'none';
    });


    // Insurance Concierge Logic
    if (insuranceBtn) insuranceBtn.addEventListener('click', (e) => {
        e.preventDefault();
        insuranceModal.classList.add('show');
    });

    if (closeInsuranceBtn) closeInsuranceBtn.addEventListener('click', () => {
        insuranceModal.classList.remove('show');
    });

    if (insuranceModal) insuranceModal.addEventListener('click', (e) => {
        if (e.target === insuranceModal) insuranceModal.classList.remove('show');
    });

    if (checkInsuranceBtn) {
        checkInsuranceBtn.addEventListener('click', async () => {
            const policyText = policyTextInput.value;
            const treatmentName = treatmentNameInput.value;

            if (!policyText || !treatmentName) {
                alert('Please provide both policy text and treatment name.');
                return;
            }

            const originalBtnContent = checkInsuranceBtn.innerHTML;
            checkInsuranceBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Auditing Policy...';
            checkInsuranceBtn.disabled = true;
            
            insuranceResult.style.display = 'block';
            insuranceResult.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--text-light);"><i class="fas fa-microscope fa-spin" style="font-size: 2rem; color: var(--primary-color); margin-bottom: 15px; display: block;"></i> <span style="font-weight: 500;">Our AI Policy Auditor is analyzing your coverage...</span></div>';

            const formData = new FormData();
            formData.append('policy_text', policyText);
            formData.append('treatment', treatmentName);
            formData.append('user_id', 'default');

            try {
                const res = await fetch('/insurance-check', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                
                if (data.status === 'success') {
                    renderInsuranceResult(data, treatmentName);
                } else {
                    insuranceResult.innerHTML = `<div style="color: #dc2626; padding: 15px; background: #fee2e2; border-radius: 12px; border: 1px solid #fecaca; display: flex; align-items: center; gap: 10px;"><i class="fas fa-exclamation-circle"></i> Error: ${data.message}</div>`;
                }
            } catch (err) {
                console.error("Insurance Audit Error:", err);
                insuranceResult.innerHTML = `<div style="color: #dc2626; padding: 15px; background: #fee2e2; border-radius: 12px; border: 1px solid #fecaca; display: flex; align-items: center; gap: 10px;"><i class="fas fa-wifi-slash"></i> Audit Error: ${err.message}</div>`;
            } finally {
                checkInsuranceBtn.innerHTML = originalBtnContent;
                checkInsuranceBtn.disabled = false;
            }
        });
    }

    function renderInsuranceResult(data, treatment) {
        const coverClass = (data.is_covered || 'unknown').toLowerCase();
        const badgeClass  = `badge-${coverClass}`;
        const headerClass = `covered-${coverClass}`;

        // Normalise fields — AI sometimes returns a string instead of an array
        const toArray = v => {
            if (!v) return [];
            if (Array.isArray(v)) return v;
            // Single string — wrap it
            return [String(v)];
        };
        const limitations   = toArray(data.limitations);
        const required_docs = toArray(data.required_docs);

        insuranceResult.innerHTML = `
            <div class="insurance-card">
                <div class="insurance-card-header ${headerClass}">
                    <h4 style="margin:0;color:var(--text-color);font-size:1rem;font-weight:600;">
                        "${treatment}" Coverage Trace
                    </h4>
                    <span class="coverage-badge ${badgeClass}">${data.is_covered || 'Unknown'}</span>
                </div>
                <div class="insurance-card-body">
                    <div class="audit-section">
                        <span class="audit-label">Policy Analysis Logic</span>
                        <div class="audit-content">${data.summary_logic || 'No details available.'}</div>
                    </div>

                    <div class="co-pay-box">
                        <span style="font-size:0.85rem;color:var(--text-light);font-weight:500;">Estimated Co-pay / Limit</span>
                        <span class="co-pay-value">${data.estimated_co_pay || 'None Discovered'}</span>
                    </div>

                    ${limitations.length > 0 ? `
                        <div class="audit-section">
                            <span class="audit-label" style="color:#f59e0b;">
                                <i class="fas fa-info-circle"></i> Conditions &amp; Waiting Periods
                            </span>
                            <ul style="padding-left:20px;margin-top:5px;color:#4b5563;font-size:0.85rem;">
                                ${limitations.map(lim => `<li style="margin-bottom:4px;">${lim}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${required_docs.length > 0 ? `
                        <div class="audit-section" style="margin-bottom:0;">
                            <span class="audit-label" style="color:#4f46e5;">
                                <i class="fas fa-file-medical"></i> Documentation Needed for Claim
                            </span>
                            <div style="margin-top:8px;">
                                ${required_docs.map(doc => `<span class="doc-tag">${doc}</span>`).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    // Symptom Cam Handler
    if (symptomCamForm) symptomCamForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = symptomImageInput.files[0];
        if (!file) {
            alert("Please select a photo first.");
            return;
        }

        const originalBtnContent = symptomCamForm.querySelector('button').innerHTML;
        symptomCamForm.querySelector('button').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        symptomCamForm.querySelector('button').disabled = true;
        
        symptomCamResult.style.display = 'block';
        symptomCamResult.innerHTML = '<div style="text-align: center; padding: 20px;"><i class="fas fa-camera fa-spin" style="font-size: 2rem; color: var(--primary-color);"></i><p style="margin-top:10px;">Our AI is examining the symptom photo...</p></div>';

        const formData = new FormData();
        formData.append('image', file);
        formData.append('symptoms_history', symptomContext.value);
        formData.append('user_id', 'default');

        try {
            const res = await fetch('/symptom-cam', { method: 'POST', body: formData });
            const data = await res.json();
            renderSymptomCamResult(data);
        } catch (err) { 
            symptomCamResult.innerHTML = `<div style="color: #dc2626; padding: 10px; background: #fee2e2; border-radius: 8px;">Error: ${err.message}</div>`;
        } finally {
            symptomCamForm.querySelector('button').innerHTML = originalBtnContent;
            symptomCamForm.querySelector('button').disabled = false;
        }
    });

    // Medication Safety Handler
    if (verifyMedSafetyBtn) verifyMedSafetyBtn.addEventListener('click', async () => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-box';
        resultDiv.style.marginTop = '15px';
        verifyMedSafetyBtn.parentNode.appendChild(resultDiv);
        resultDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running cross-medication safety audit...';

        try {
            const res = await fetch('/check-medication-safety', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: 'default', medication_name: 'ALL', is_comprehensive: true })
            });
            const data = await res.json();
            if (data.is_safe) {
                resultDiv.innerHTML = `<div style="color: #059669; padding: 15px; background: #ecfdf5; border-radius: 12px; border: 1px solid #d1fae5;"><i class="fas fa-check-circle"></i> ${data.summary}</div>`;
            } else {
                resultDiv.innerHTML = `<div style="color: #dc2626; padding: 15px; background: #fef2f2; border-radius: 12px; border: 1px solid #fee2e2;"><i class="fas fa-exclamation-triangle"></i> <strong>Safety Alert!</strong><br>${marked.parse(data.summary)}</div>`;
            }
        } catch (err) { 
            resultDiv.innerHTML = `<div style="color: #dc2626; padding: 10px; background: #fee2e2; border-radius: 8px;">Error: ${err.message}</div>`;
        }
    });
});
