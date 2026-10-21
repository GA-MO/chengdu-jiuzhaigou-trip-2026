# Chengdu trip, 7–14 Nov 2026

Offline-first itinerary for Chengdu, Bipenggou, Dagu Glacier and Jiuzhaigou. One static page, no build step.

- `index.html`: the app (plan, flights, edit screen)
- `sw.js`: service worker for offline use
- `fonts/`: Bodoni Moda and Trirong (Thai only), all SIL Open Font License (`fonts/OFL*.txt`), self-hosted so they work offline

Edits made on the phone (times, booking numbers, saved places and phrases, your own bank rate) are stored in the browser only. The yuan to baht rate refreshes from open.er-api.com at most once a day when online.
