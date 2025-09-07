# Smart Insurance Onboarding (BJAK demo)

A one-page onboarding experience with expandable sections: Car Plate → Personal Info → Car Info → Funding. Built with React + Vite and vanilla CSS. Back-end contracts are in `src/api.js`.

## Run
```bash
npm install
npm run dev
```

## API Endpoints
- POST `/verify-plate` → { status: 'existing'|'new'|'invalid', existingProfile? }
- POST `/validate-car` → { ok: true, corrected?, message? }
- POST `/submit-onboarding` → { ok: true, applicationId } | { ok:false, message }

## Notes
- Plate normalization: uppercase, no spaces; client validates basic pattern.
- NRIC parsing derives gender & DOB (best-effort heuristics).
- Postcode → city/state has a light hint map; replace with backend.
