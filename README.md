# NavJeevan — Rural & Underserved Healthcare Access Intelligence Platform

> **TURING HACKX 2026 — HealthTech Track**
> **Team:** Code Catalyst · **Members:** Prakhar Gupta, Aditya Dubey

NavJeevan is a **multilingual, offline-first healthcare access platform** built for rural and underserved communities in India — where connectivity is weak, digital literacy is low, and quality care is often hours away.

It connects patients, ASHA workers, doctors, pharmacies and facilities into one unified network — so the right care reaches the right person, even on a low-end phone with intermittent internet.

---

## The Problem

- **Poor connectivity** — large parts of rural India have weak or no home internet.
- **Unnecessary travel & waiting** — patients travel long distances only to find no doctor, no medicine, or a closed clinic.
- **Low digital literacy** — app-first designs exclude elderly and low-literacy users.
- **Fragmented records** — health history is scattered across paper and disconnected systems.

---

## Our Solution — an Intelligence Layer over Healthcare Access

| Capability | How it works |
|---|---|
| **Unified Healthcare Network** | Connects patients, ASHA workers, doctors, pharmacies and facilities in one ecosystem. |
| **Teleconsultation** | Video, audio and text consultations tuned for low-bandwidth areas. |
| **Offline Health Records** | Stores records on-device and syncs automatically the moment connectivity returns. |
| **Healthcare Availability** | Live view of doctors, appointments, diagnostics and medicine stock. |
| **AI-Assisted Triage** | Preliminary symptom assessment with clear uncertainty labels and **professional oversight**. |
| **Smart Routing** | Directs patients to suitable facilities and manages appointments/queues. |
| **Caregiver Support** | Lets families manage treatment, records and follow-ups on behalf of elderly or dependent patients. |

---

## Technology Stack

- **React Native** — cross-platform mobile app for Android & iOS
- **Node.js + Django APIs** — backend services
- **TensorFlow Lite** — lightweight on-device AI symptom checker that runs on resource-constrained rural phones
- **SQLite** — offline local storage, with automatic cloud sync
- **SMS API (Textbee / Twilio)** — no-internet fallback channel for alerts, follow-ups and queue updates
- **ABHA integration** — digital health records aligned with India's Ayushman Bharat stack

---

## Feasibility

- **Offline-first:** core features work with weak or intermittent internet.
- **Multi-channel:** video, audio, text and SMS adapt to whatever bandwidth is available.
- **ASHA support:** enables onboarding, assisted use and follow-ups for low-literacy users.
- **Lightweight AI:** model runs on resource-constrained smartphones via TFLite.
- **Modular design:** deployable across districts and healthcare networks.

---

## Key Challenges & How We Mitigate Them

| Challenge | Mitigation |
|---|---|
| Low digital literacy | Voice UI + simple workflows + ASHA worker support |
| Poor connectivity | Offline storage + auto-sync + SMS fallback |
| Elderly users | Caregiver support + accessible interface |
| Stale availability data | Provider updates + timestamps + validation |
| AI safety | Uncertainty labels + professional verification |
| Privacy | Consent-based access + encryption + role permissions |
| Healthcare overload | Smart queues + priority-based routing |

---

## Who It Helps

**Patients**
- Less unnecessary travel and waiting
- Faster access to appropriate care
- Better visibility of doctors, specialists, medicines and diagnostics
- Accessible digital health records

**Caregivers & Families**
- Assist elderly, dependent and low-literacy patients
- Manage appointments, records and follow-ups with patient consent

**Doctors & Specialists**
- Better-organized appointments and queues
- Access to relevant patient history with consent
- Remote and asynchronous consultation support

**ASHA / Community Health Workers**
- Digital tools for onboarding, referrals and follow-ups
- Stronger connection between underserved communities and formal healthcare services

---

## References

- CEDA, Ashoka University — *One Nation, Many Disconnects: Mapping India's Home Internet Gaps*
  <https://ceda.ashoka.edu.in/one-nation-many-disconnects-mapping-indias-home-internet-gaps>
- Rural Health Information Hub — *Telehealth / Health IT*
  <https://www.ruralhealthinfo.org/topics/telehealth-health-it>
- IZA Discussion Paper 15387 — supporting research material used in the original concept
  <https://docs.iza.org/dp15387.pdf>

---

## Current Prototype

This repository contains an early working prototype of NavJeevan's AI-assisted triage core: on-device symptom/condition classification for skin and hair conditions, appointment scheduling, healthcare facility discovery, and an AI wellness coach — demonstrating the image-based triage and patient-facing workflows the full platform is built around.

> Health advice is for guidance only and is always reviewed by healthcare professionals. NavJeevan is not a substitute for professional medical advice.
