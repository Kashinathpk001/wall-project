// CAN YOU LEAN ON? // TR-89 WALL CHECKER
// INTERACTIVE ENGINE & LIVE PREVIEW

const SPECIMEN_PROFILES = {
    pazhampori: {
        location: "Canteen Pazhampori Counter",
        thickness: 230,
        age: 18,
        height: 3.2,
        cracks: 1,
        repairs: 0,
        dampness: "0",
        chalkRisk: 64,
        moisture: 18,
        sneeze: 82,
        gossipCount: "4,820",
        gossipPct: 76,
        score: 80,
        verdict: "SAFE TO LEAN ON",
        verdictClass: "verdict-banner-pass",
        archetype: "The Pazhampori Sentry",
        desc: "Hot coconut oil steam and 4 PM chai chats. The wall won't fall, but your shirt might smell like fried banana."
    },
    lecture: {
        location: "Lecture Hall 101 Backrow",
        thickness: 150,
        age: 6,
        height: 3.6,
        cracks: 0,
        repairs: 2,
        dampness: "0",
        chalkRisk: 12,
        moisture: 8,
        sneeze: 90,
        gossipCount: "2,680",
        gossipPct: 42,
        score: 90,
        verdict: "SAFE TO LEAN ON",
        verdictClass: "verdict-banner-pass",
        archetype: "Nap Polish Certified",
        desc: "Buffed smooth by thousands of sleeping students. Near-zero friction and minimal chalk dust."
    },
    hostel: {
        location: "Hostel Cricket Corridor",
        thickness: 200,
        age: 24,
        height: 2.9,
        cracks: 7,
        repairs: 4,
        dampness: "0",
        chalkRisk: 88,
        moisture: 22,
        sneeze: 45,
        gossipCount: "6,450",
        gossipPct: 92,
        score: 35,
        verdict: "BE CAREFUL (MIGHT BREAK)",
        verdictClass: "verdict-banner-fail",
        archetype: "The Comeback Story",
        desc: "Has survived 14 midnight cricket matches and tennis ball hits. Held together by spackle and prayer."
    },
    library: {
        location: "Library Exam Silent Corner",
        thickness: 300,
        age: 12,
        height: 4.0,
        cracks: 0,
        repairs: 0,
        dampness: "1",
        chalkRisk: 20,
        moisture: 72,
        sneeze: 96,
        gossipCount: "3,940",
        gossipPct: 58,
        score: 75,
        verdict: "MOSTLY SAFE",
        verdictClass: "verdict-banner-pass",
        archetype: "The Weeping Philosopher",
        desc: "Solid reinforced concrete, but slightly cold and damp from years of collective GPA panic tears."
    },
    washroom: {
        location: "Campus Washroom Stall Partition",
        thickness: 45,
        age: 32,
        height: 2.2,
        cracks: 14,
        repairs: 6,
        dampness: "1",
        chalkRisk: 95,
        moisture: 92,
        sneeze: 10,
        gossipCount: "8,120",
        gossipPct: 98,
        score: 10,
        verdict: "DO NOT LEAN (TOO THIN)",
        verdictClass: "verdict-banner-fail",
        archetype: "The Betrayer",
        desc: "45mm of thin plywood covered in cheat notes. One sharp lean and you'll fall into the next stall."
    },
    fee: {
        location: "College Fee & Accounts Counter",
        thickness: 450,
        age: 45,
        height: 3.5,
        cracks: 0,
        repairs: 0,
        dampness: "0",
        chalkRisk: 5,
        moisture: 5,
        sneeze: 100,
        gossipCount: "9,870",
        gossipPct: 100,
        score: 100,
        verdict: "SOLID STONE (100% SAFE)",
        verdictClass: "verdict-banner-pass",
        archetype: "The Impenetrable Stonewall",
        desc: "450mm granite stone counter. Completely immovable and solid."
    }
};

// Select Specimen Preset
function selectPreset(type, btnEl) {
    const spec = SPECIMEN_PROFILES[type];
    if (!spec) return;

    // Highlight active preset button
    document.querySelectorAll('.eng-preset-btn').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');

    // Populate active form
    const form = document.getElementById('workbenchForm') || document.getElementById('inspectForm');
    if (form) {
        const setVal = (id, val) => {
            const el = form.querySelector(`#${id}`);
            if (el) el.value = val;
        };

        setVal('wall-location', spec.location);
        setVal('wall-thickness', spec.thickness);
        setVal('wall-age', spec.age);
        setVal('wall-height', spec.height);
        setVal('wall-cracks', spec.cracks);
        setVal('wall-repairs', spec.repairs);
        setVal('wall-dampness', spec.dampness);
    }

    // Update Telemetry Panel
    updateTelemetry(spec);
}

// Update Telemetry Displays
function updateTelemetry(spec) {
    const scoreNum = document.getElementById('tele-score-num');
    const projScore = document.getElementById('tele-projected-score');
    const verdBanner = document.getElementById('tele-verdict-banner');
    const chalkVal = document.getElementById('tele-chalk-val');
    const chalkBar = document.getElementById('tele-chalk-bar');
    const moistVal = document.getElementById('tele-moisture-val');
    const moistBar = document.getElementById('tele-moisture-bar');
    const sneezeVal = document.getElementById('tele-sneeze-val');
    const sneezeBar = document.getElementById('tele-sneeze-bar');
    const gossipVal = document.getElementById('tele-gossip-val');
    const gossipBar = document.getElementById('tele-gossip-bar');
    const archTitle = document.getElementById('tele-arch-name');
    const archDesc = document.getElementById('tele-arch-desc');

    if (scoreNum && spec.score !== undefined) scoreNum.textContent = spec.score;
    if (projScore && spec.score !== undefined) projScore.textContent = `EST: ${spec.score}/100`;

    if (verdBanner && spec.verdict) {
        verdBanner.textContent = `● ${spec.verdict}`;
        verdBanner.className = `telemetry-verdict-banner ${spec.verdictClass || 'verdict-banner-pass'}`;
    }

    if (chalkBar && chalkVal && spec.chalkRisk !== undefined) {
        chalkBar.style.width = `${spec.chalkRisk}%`;
        chalkVal.textContent = spec.chalkRisk > 70 ? `HIGH CHALK (${spec.chalkRisk}%)` : spec.chalkRisk > 40 ? `MEDIUM (${spec.chalkRisk}%)` : `LOW / CLEAN (${spec.chalkRisk}%)`;
        chalkBar.className = `eng-bar-fill ${spec.chalkRisk > 70 ? 'red' : spec.chalkRisk > 40 ? 'yellow' : 'green'}`;
    }

    if (moistBar && moistVal && spec.moisture !== undefined) {
        moistBar.style.width = `${spec.moisture}%`;
        moistVal.textContent = spec.moisture > 60 ? `SOAKING WET (${spec.moisture}%)` : spec.moisture > 30 ? `DAMP (${spec.moisture}%)` : `DRY (${spec.moisture}%)`;
        moistBar.className = `eng-bar-fill ${spec.moisture > 60 ? 'red' : spec.moisture > 30 ? '' : 'green'}`;
    }

    if (sneezeBar && sneezeVal && spec.sneeze !== undefined) {
        sneezeBar.style.width = `${spec.sneeze}%`;
        sneezeVal.textContent = spec.sneeze > 70 ? `SOLID (${spec.sneeze}%)` : spec.sneeze > 40 ? `SHAKY (${spec.sneeze}%)` : `COLLAPSE RISK (${spec.sneeze}%)`;
        sneezeBar.className = `eng-bar-fill ${spec.sneeze > 70 ? 'green' : spec.sneeze > 40 ? 'yellow' : 'red'}`;
    }

    if (gossipVal && spec.gossipCount !== undefined) {
        gossipVal.textContent = `${spec.gossipCount} SECRETS`;
    }
    if (gossipBar && spec.gossipPct !== undefined) {
        gossipBar.style.width = `${spec.gossipPct}%`;
    }

    if (archTitle && spec.archetype) archTitle.textContent = spec.archetype;
    if (archDesc && spec.desc) archDesc.textContent = spec.desc;
}

// Test-Lean Simulator for Hackathon
function simulateLean() {
    const scoreEl = document.getElementById('tele-score-num');
    const score = parseInt(scoreEl ? scoreEl.textContent : '80', 10);
    const simBox = document.getElementById('sim-result-box');
    if (!simBox) return;

    document.body.classList.remove('screen-shake');
    simBox.innerHTML = '<span style="color: var(--yellow);">⏳ Applying 72kg of slouching student weight against wall...</span>';

    setTimeout(() => {
        if (score >= 70) {
            simBox.innerHTML = '<strong style="color: var(--green);">✅ CLINK! Solid support. Zero chalk transfer. Your spine is smiling.</strong>';
        } else if (score >= 40) {
            simBox.innerHTML = '<strong style="color: var(--yellow);">⚠️ CREAK... The wall groaned. A small cloud of white chalk fell onto your shoulder.</strong>';
        } else {
            document.body.classList.add('screen-shake');
            simBox.innerHTML = '<strong style="color: var(--red);">💥 CRUNCH! The wall cracked 2 centimeters. Run before the college principal arrives!</strong>';
            setTimeout(() => {
                document.body.classList.remove('screen-shake');
            }, 500);
        }
    }, 400);
}

// Client-Side Search Filter for Database
function filterWalls() {
    const input = document.getElementById('wallSearch');
    if (!input) return;
    const filter = input.value.toLowerCase();
    const table = document.getElementById('wallsTable');
    if (!table) return;

    const trs = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
    for (let i = 0; i < trs.length; i++) {
        const text = trs[i].textContent.toLowerCase();
        trs[i].style.display = text.includes(filter) ? '' : 'none';
    }
}

// System Boot on DOM Loaded
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Boot Initialization Curtain
    const curtain = document.getElementById('intro-curtain');
    const fillBar = document.getElementById('intro-loading-fill');
    const statusText = document.getElementById('intro-status-text');

    if (curtain) {
        if (fillBar) {
            requestAnimationFrame(() => {
                fillBar.style.width = '100%';
            });
        }

        const bootMessages = [
            "CHECKING WALL STABILITY...",
            "SNIFFING CHAI VAPORS & STEAM...",
            "CHECKING IF YOUR SHIRT WILL GET WHITE CHALK...",
            "READY TO LEAN!"
        ];

        let msgIdx = 0;
        const msgInterval = setInterval(() => {
            msgIdx++;
            if (msgIdx < bootMessages.length && statusText) {
                statusText.style.opacity = '0';
                setTimeout(() => {
                    if (statusText) {
                        statusText.textContent = bootMessages[msgIdx];
                        statusText.style.opacity = '1';
                    }
                }, 100);
            }
        }, 320);

        let dismissed = false;
        const revealUI = () => {
            if (dismissed) return;
            dismissed = true;
            clearInterval(msgInterval);
            if (statusText) statusText.textContent = "READY TO LEAN!";
            if (fillBar) fillBar.style.width = '100%';

            curtain.classList.add('hidden');
            setTimeout(() => {
                curtain.style.display = 'none';
            }, 850);
        };

        const autoTimer = setTimeout(revealUI, 1600);

        curtain.addEventListener('click', () => {
            clearTimeout(autoTimer);
            revealUI();
        });

        window.addEventListener('keydown', () => {
            if (!dismissed) {
                clearTimeout(autoTimer);
                revealUI();
            }
        }, { once: true });
    }

    // 2. Mouse Spotlight on Panels & Cards
    const cards = document.querySelectorAll('.eng-panel, .scale-specimen-card, .dossier-sheet, .eng-preset-btn');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    // 3. Result Page Animated Count-Up Score & Meter Fill
    const scoreNumEl = document.getElementById('countup-score');
    const meterFillEl = document.getElementById('meter-fill');
    if (scoreNumEl) {
        const rawTarget = scoreNumEl.getAttribute('data-target');
        const targetScore = parseInt(rawTarget !== null ? rawTarget : '0', 10);
        let current = 0;
        scoreNumEl.textContent = '0';
        if (meterFillEl) meterFillEl.style.width = '0%';
        const duration = 1200; // ms
        const startTime = performance.now();

        function updateScore(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            current = Math.round(easeOut * targetScore);
            scoreNumEl.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(updateScore);
            } else {
                scoreNumEl.textContent = targetScore;
            }
        }
        requestAnimationFrame(updateScore);

        if (meterFillEl) {
            setTimeout(() => {
                meterFillEl.style.width = `${targetScore}%`;
            }, 80);
        }
    }

    // 4. Scanner Dialog on Form Submit
    const forms = document.querySelectorAll('#workbenchForm, #inspectForm');
    const scanModal = document.getElementById('scan-modal');
    const scanStatus = document.getElementById('scan-status-text');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!scanModal) return;
            e.preventDefault();

            scanModal.style.display = 'flex';

            const scanSteps = [
                "📐 Measuring wall thickness...",
                "💧 Checking if the wall is wet or sweating...",
                "🏏 Checking if it can handle someone leaning on it...",
                "👕 Checking white chalk powder on shirt risk...",
                "✨ Almost done..."
            ];

            let stepIdx = 0;
            const scanInterval = setInterval(() => {
                stepIdx++;
                if (stepIdx < scanSteps.length && scanStatus) {
                    scanStatus.style.opacity = '0';
                    setTimeout(() => {
                        if (scanStatus) {
                            scanStatus.textContent = scanSteps[stepIdx];
                            scanStatus.style.opacity = '1';
                        }
                    }, 80);
                }
            }, 240);

            setTimeout(() => {
                clearInterval(scanInterval);
                HTMLFormElement.prototype.submit.call(form);
            }, 1250);
        });
    });

    // 5. UTC Clock in System Header
    const clockEl = document.getElementById('sys-clock');
    if (clockEl) {
        const tick = () => {
            const now = new Date();
            clockEl.textContent = now.toISOString().substring(11, 19) + ' UTC';
        };
        tick();
        setInterval(tick, 1000);
    }

    // 6. Real-Time Telemetry Recalculation on Input
    const activeForm = document.getElementById('workbenchForm') || document.getElementById('inspectForm');
    if (activeForm) {
        const recalculate = () => {
            const thickness = parseInt(activeForm.querySelector('#wall-thickness')?.value || '200', 10);
            const cracks = parseInt(activeForm.querySelector('#wall-cracks')?.value || '0', 10);
            const dampness = activeForm.querySelector('#wall-dampness')?.value;
            const age = parseInt(activeForm.querySelector('#wall-age')?.value || '10', 10);

            let score = 100;
            if (age >= 20) score -= 15;
            else if (age >= 10) score -= 10;

            if (cracks >= 6) score -= 35;
            else if (cracks >= 3) score -= 20;
            else if (cracks >= 1) score -= 10;

            if (dampness === '1') score -= 15;
            if (thickness < 150) score -= 10;
            score = Math.max(0, Math.min(100, score));

            let chalk = 20;
            if (age > 20) chalk += 30;
            if (cracks > 3) chalk += 25;
            chalk = Math.min(chalk, 100);

            const shirtColor = activeForm.querySelector('#shirt-color')?.value || 'black';
            const shirtMult = {
                black: 1.0,
                navy: 0.9,
                gray: 0.5,
                white: 0.15,
                silk: 1.0
            }[shirtColor] || 0.8;
            const finalChalk = Math.min(100, Math.round(chalk * shirtMult));

            const moisture = (dampness === '1') ? 78 : 12;
            const sneeze = Math.max(10, Math.min(100, Math.round((thickness / 3) - (cracks * 7))));
            const gossipTotal = Math.round(age * 210 + cracks * 145 + 1420);
            const gossipPct = Math.min(100, Math.round((gossipTotal / 9500) * 100));

            let verdict = "SAFE TO LEAN ON";
            let vClass = "verdict-banner-pass";
            if (score < 40) {
                verdict = "DO NOT LEAN (TOO WEAK)";
                vClass = "verdict-banner-fail";
            } else if (score < 60) {
                verdict = "BE CAREFUL (LIGHT LEAN ONLY)";
                vClass = "verdict-banner-caution";
            } else if (score < 80) {
                verdict = "MOSTLY SAFE";
                vClass = "verdict-banner-pass";
            }

            updateTelemetry({
                score: score,
                verdict: verdict,
                verdictClass: vClass,
                chalkRisk: finalChalk,
                moisture: moisture,
                sneeze: sneeze,
                gossipCount: gossipTotal.toLocaleString(),
                gossipPct: gossipPct,
                archetype: "Custom Wall",
                desc: "Real-time estimate based on the measurements you entered."
            });
        };

        activeForm.querySelectorAll('input, select').forEach(el => {
            el.addEventListener('input', recalculate);
            el.addEventListener('change', recalculate);
        });
    }
});
