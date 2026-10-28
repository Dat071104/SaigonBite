# Domain connection — 28 October 2026

Deployed by Codex (AI-assisted), in Dat's session. Tenten account belongs to Dat; the existing GCP VM uses the separately configured school account.

- DNS: Tenten `@` A and `www` A both point to `34.21.141.239`; screenshot `tenten-dns.png`; authoritative Tenten and public resolvers returned the address. Domain active, registration profile confirmed, expires 28 October 2027, automatic renewal off.
- Main HTTPS returned 200 with a verified Let's Encrypt YE2 certificate, expires 26 January 2027 02:42:14 UTC; HTTP redirected with 308. `https://www.saigonbite.io.vn/` returned 301 to the apex; sslip.io fallback returned 200. Caddy automatically renews certificates while DNS and VM remain available.
- New VM release `p6-deploy-20261028`, commit `55df8ae431aa2288c562cc4d82d702bc4cc97aad`, image `sha256:432106755fdf4bf9802a87f0484ea8f39705ae9a938c8a5bf740d1a598add619`, bundle SHA-256 `d68953ef6f580050202245f8d3a98c0a81f638901e1d840fe60d4e81a376e626` verified locally and remotely. Existing deploy script requires tag prefix p6-deploy. Local only; no push.
- Pre-deploy online backup `saigonbite-20261028T033955Z.db.gz` passed integrity check and uploaded to the existing bucket. Order 9's state and monetary fields matched before and after deployment. Containers running, app healthy, backup timer enabled; `vm-before-csrf.txt`, `vm-after-csrf.txt`.
- Cookie Secure, HttpOnly, SameSite=Lax; invalid CSRF returned 400 and the logical SQLite database digest was identical before/after; `security_public.json`, `invalid_csrf.png`. This does not assert non-database effects.
- The first HTTPS probes occurred while Caddy was obtaining certificates and failed; Caddy then reported successful issuance for both names and the subsequent probes passed. No GCP resource, firewall or billing change. IAP's temporary project SSH key was removed after matching its sole entry; empty metadata was verified. See `Part2/notes/P6/gcloud_log.md`.
- The previous P6 evidence remains a historical record of that earlier release and fallback URL. Domain expiry is not VM lifetime: free trial expires 21 January 2027 unless the owner makes another authorized arrangement.
