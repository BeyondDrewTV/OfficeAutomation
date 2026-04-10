# Starter Website — Publish Checklist

Run through this in order before declaring the site live.
Every item must be checked. If something fails, fix it and re-check — do not skip forward.

---

## Stage 1: Pre-Publish Review

Complete this before touching DNS or hosting.

**Content**
- [ ] All sections match the approved content intake form — no placeholder text anywhere
- [ ] Business name spelled correctly throughout
- [ ] Phone number is correct and formatted consistently
- [ ] Service list matches what was agreed in intake
- [ ] Testimonials attributed correctly (names/initials match what client approved)
- [ ] No Lorem Ipsum, "Your Name Here", or template placeholder text anywhere on the page

**Links and functionality**
- [ ] Primary CTA button works (phone link dials, form submits, or email opens correctly)
- [ ] All internal anchor links scroll to the correct section
- [ ] No broken image references (all images load correctly)
- [ ] Logo loads correctly in the header

**Mobile QA**
- [ ] Page loads and renders correctly at 375px (iPhone SE baseline)
- [ ] Page loads and renders correctly at 390px (iPhone 14 baseline)
- [ ] Page loads and renders correctly at 768px (tablet)
- [ ] Text is readable at all sizes — no overflow or clipping
- [ ] CTA button is tappable and full-width on mobile
- [ ] Navigation or page sections are accessible without horizontal scrolling

**Contact CTA tested**
- [ ] Drew tested the contact CTA end-to-end:
  - If phone: dialed the number from a real phone
  - If form: submitted a test entry and confirmed it arrived at the destination
  - If email: clicked the email link and confirmed the address is correct
- [ ] Form submissions go to the correct destination (email or sheet)
- [ ] No test submissions left in the live destination before handoff

---

## Stage 2: Domain and DNS

**DNS**
- [ ] DNS A record or CNAME pointed to the correct host/IP
- [ ] DNS propagation confirmed (use a checker like dnschecker.org or wait 15–60 min after update)
- [ ] Old site redirected if the client had a previous site at this domain: [ ] Yes / [ ] N/A

**HTTPS**
- [ ] SSL certificate is active — site loads at `https://` with no browser warning
- [ ] `http://` redirects to `https://` automatically

**Domain confirmation**
- [ ] Site loads at the correct URL (not a staging URL, preview URL, or subdomain)
- [ ] Domain owner confirmed (client owns the registrar account or transfer is complete)

---

## Stage 3: Post-Launch Verification

Run these checks after DNS has propagated and the site is live at the real URL.

- [ ] Site loads correctly at the live URL on a desktop browser
- [ ] Site loads correctly at the live URL on the owner's phone
- [ ] Contact CTA works end-to-end from the live URL (not just from a local or preview build)
- [ ] Form submission (if applicable) confirmed received at the correct destination from the live URL
- [ ] No console errors that affect user-facing functionality
- [ ] Page title and meta description are set and accurate (not template defaults)

---

## Stage 4: Launch Confirmation

- [ ] Owner has loaded the live site on their own phone and confirmed it looks correct
- [ ] Owner has tested the contact CTA themselves
- [ ] Launch screenshot captured and stored (file name / location):
- [ ] Owner notified that the site is live — date and method:
- [ ] Any test submissions cleared from the form destination

---

## Publish Checklist Sign-Off

**Date launched:**
**Live URL:**
**Drew:**
**Owner confirmed:**

> Keep this completed checklist on file. It is referenced in the handoff closeout.
