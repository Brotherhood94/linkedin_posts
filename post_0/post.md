# LinkedIn post — Two-Tower Matrix Multiplication

**Type:** Research / preprint drop (Template #1)
**Language:** English
**Target length:** ~1,300 chars (research drops can sit at the upper end)
**Media:** `two_tower.gif` (intuition for K=3)
**First-comment link:** GitHub + arxiv (once available) → `https://github.com/Brotherhood94/two_tower_quantum_matrix_multiplication_subroutine`

---

## The post (copy-paste ready)

🎊 𝗡𝗲𝘄 𝗽𝗿𝗲𝗽𝗿𝗶𝗻𝘁 𝗶𝘀 𝗼𝘂𝘁! 🎊
🏗️ 𝙏𝙬𝙤-𝙏𝙤𝙬𝙚𝙧 𝙈𝙖𝙩𝙧𝙞𝙭 𝙈𝙪𝙡𝙩𝙞𝙥𝙡𝙞𝙘𝙖𝙩𝙞𝙤𝙣: 𝗮 𝗾𝘂𝗮𝗻𝘁𝘂𝗺 𝘀𝘂𝗯𝗿𝗼𝘂𝘁𝗶𝗻𝗲 𝗳𝗼𝗿 #matrix 𝗰𝗵𝗮𝗶𝗻 𝗽𝗿𝗼𝗱𝘂𝗰𝘁𝘀 𝘄𝗶𝘁𝗵 𝗰𝗶𝗿𝗰𝘂𝗶𝘁 𝗱𝗲𝗽𝘁𝗵 𝗶𝗻𝗱𝗲𝗽𝗲𝗻𝗱𝗲𝗻𝘁 𝗼𝗳 𝘁𝗵𝗲 𝗰𝗵𝗮𝗶𝗻 𝗹𝗲𝗻𝗴𝘁𝗵.

🤔 𝘈𝘳𝘦 𝘺𝘰𝘶 𝘢 𝘲𝘶𝘢𝘯𝘵𝘶𝘮 𝘢𝘭𝘨𝘰𝘳𝘪𝘵𝘩𝘮 𝘥𝘦𝘴𝘪𝘨𝘯𝘦𝘳 𝘮𝘶𝘭𝘵𝘪𝘱𝘭𝘺𝘪𝘯𝘨 𝘢 𝘤𝘩𝘢𝘪𝘯 𝘰𝘧 𝘮𝘢𝘵𝘳𝘪𝘤𝘦𝘴 𝓦 = 𝙈⁽⁰⁾·…·𝙈⁽ᴷ⁻¹⁾ ?

⛔ Classically, 𝗞 distinct N×N matrices cost 𝙊(𝙆·𝙉^ω) operations. Existing quantum approaches still pay a price that 𝙜𝙧𝙤𝙬𝙨 𝙬𝙞𝙩𝙝 𝙆 — typically 𝙊(𝙆·polylog 𝙉) depth in the block-encoding model.

🛠️ We propose a different 𝙩𝙧𝙖𝙙𝙚-𝙤𝙛𝙛: interleave state-preparation operators across 𝘁𝘄𝗼 𝗹𝗮𝘆𝗲𝗿𝘀 ("𝘵𝘩𝘦 𝘵𝘸𝘰 𝘵𝘰𝘸𝘦𝘳𝘴"). Within each layer, operators act on 𝗱𝗶𝘀𝗷𝗼𝗶𝗻𝘁 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝘀 and run in 𝗽𝗮𝗿𝗮𝗹𝗹𝗲𝗹.

🔑 The Kronecker identity vec(𝘼𝙓𝘽) = (𝘽ᵀ ⊗ 𝘼)·vec(𝙓), applied recursively, lets us encode the entire chain product as amplitudes of a single quantum state.

🚀 𝗧𝗵𝗲 𝗿𝗲𝘀𝘂𝗹𝘁:
― 🟣 Circuit depth 𝓞(polylog 𝙉), 𝗶𝗻𝗱𝗲𝗽𝗲𝗻𝗱𝗲𝗻𝘁 𝗼𝗳 𝗞;
― 🟣 𝚯(𝗞·𝗹𝗼𝗴 𝗡) qubits (exponential compression vs 𝙊(𝙆·𝙉²) classical memory);
― 🟣 No optimal parenthesisation needed (vs 𝙊(𝙆³) classical ordering);
― 🟣 Open-source #Qiskit + #QCLAB implementations.

📌 Submitted to #ESA2026.

🧐 𝘞𝘢𝘯𝘵 𝘵𝘰 𝘴𝘦𝘦 𝘵𝘩𝘦 𝘵𝘸𝘰 𝘵𝘰𝘸𝘦𝘳𝘴 𝘪𝘯 𝘢𝘤𝘵𝘪𝘰𝘯?
📺 The GIF gives the intuition for K=3.
👉🏻👉🏻 𝗣𝗿𝗲𝗽𝗿𝗶𝗻𝘁 + 𝗰𝗼𝗱𝗲 in the first comment!

🙏 Huge thanks to my co-authors Giacomo Antonioli, Anna Bernasconi, Gianna M. Del Corso, and Alessandro Poggiali — Department of Computer Science, Università di Pisa.

---

## First-comment text

👇🏻 As promised:

🔗 Code (Qiskit + QCLAB): https://github.com/Brotherhood94/two_tower_quantum_matrix_multiplication_subroutine
📄 Preprint: <arxiv link once available>

---

## Notes for review before publishing

- Replace co-author names with tagged @ mentions on LinkedIn so they get notified
- Add the arxiv link to the first comment as soon as it's live
- Consider shortening the GitHub URL with bit.ly to track clicks (per `good_approaches.md` rule 6)
- Verify the GIF renders correctly on the LinkedIn preview before publishing
