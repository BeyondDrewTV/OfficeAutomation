# Starter Website — Domain & Hosting Decision Worksheet

Complete this before the site build begins. These decisions block deployment.
A site cannot go live until every section below is resolved.

---

## 1. Domain Status

**Does the client own a domain?**
- [ ] Yes — client owns a domain
  - Domain name:
  - Registrar (GoDaddy, Namecheap, Google Domains, Cloudflare, etc.):
  - Login access method (credentials shared / DNS delegated / transfer initiated):
  - Domain expiration date:

- [ ] No — domain purchase needed
  - Chosen domain name:
  - Registrar where Drew will register it:
  - Who pays for registration (client card / Drew bills client / Drew advances and invoices):
  - Billing owner going forward (client renews directly / Drew-managed renewal):

> Scope ceiling: The client owns their domain always. If Drew purchases it on the client's behalf, the registrar account must be in the client's name or transferred to the client at closeout. Drew-managed billing requires written acknowledgment from the client.

---

## 2. Hosting

**Who manages hosting?**

- [ ] Drew-managed (recommended)
  - Host platform (Netlify / GitHub Pages / shared host):
  - Cost per month or year:
  - Who is billed (client card on file / Drew invoices client monthly):
  - Drew retains deploy access for the life of the engagement

- [ ] Client-managed
  - Host platform:
  - Client has login access confirmed: [ ] Yes
  - Drew has deploy access confirmed: [ ] Yes / [ ] Not needed (client deploys from files Drew delivers)
  - Client is responsible for renewals, uptime, and host fees going forward

> Drew-managed hosting is the default recommendation. It simplifies deployment, SSL, and future edits. If the client insists on self-managed, confirm they have a host, can handle DNS, and understand they are responsible for uptime.

---

## 3. Contact Route

**How will site visitors contact the business?**

Choose one primary contact route. This must be wired and tested before go-live.

- [ ] Phone call only — CTA button is a `tel:` link
  - Phone number displayed and linked:

- [ ] Email CTA — CTA button opens email client
  - Email address:

- [ ] Contact form → email destination
  - Form submissions go to this email:
  - Backup: form sends to this secondary email (optional):

- [ ] Contact form → Google Sheet
  - Sheet URL:
  - Drew has edit access: [ ] Yes
  - Owner notification email when form submits:

> Only one primary contact route is in scope. Adding a second contact method (e.g., form + chat widget) is a change order.

---

## 4. DNS Management

**Who manages DNS records?**

- [ ] Drew manages DNS (recommended when Drew-managed hosting)
  - DNS is pointed by Drew at go-live
  - Registrar login or DNS delegation confirmed: [ ] Yes

- [ ] Client manages DNS
  - Drew provides the DNS records needed
  - Client confirms they can log in and make DNS changes: [ ] Yes
  - Drew is not responsible for DNS propagation delays after records are handed over

> Drew's default: Drew manages DNS for the duration of hosting. At project closeout, Drew documents the current DNS state and transfers access to the client if they want it.

---

## 5. Scope Ceiling Acknowledgment

The client must acknowledge the following before the project begins:

- Domain purchase and hosting billing are either on the client's account or explicitly acknowledged as Drew-managed with written approval.
- If Drew is managing billing on behalf of the client, an invoice or written approval is on file before any purchase is made.
- Hosting renewals after project closeout are the client's responsibility unless an ongoing support agreement is in place.

**Client acknowledgment** (signature or written confirmation in email):
> 

**Date:**
**Drew:**

---

## Decision Worksheet Sign-Off

**All decisions confirmed:**
- [ ] Domain status resolved
- [ ] Hosting confirmed and billing owner documented
- [ ] Contact route chosen and destination confirmed
- [ ] DNS management agreed

**Date:**
**Drew:**
