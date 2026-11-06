// Site-wide settings. Change contact details here; every page picks them up.
export const CONTACT = {
  name: 'Kaustubh Hari Sethi',
  role: 'Creator of Nutrayo',
  initials: 'Ks',
  email: 'kaustubhsethi14@gmail.com',
  linkedin: 'https://www.linkedin.com/in/kaustubh-hari-sethi/',
  website: 'https://kaustubhsethi.com/',
};

/** mailto: link with a prefilled subject (and optional body). */
export function mailto(subject = 'Nutrayo feedback', body = '') {
  const q = [`subject=${encodeURIComponent(subject)}`];
  if (body) q.push(`body=${encodeURIComponent(body)}`);
  return `mailto:${CONTACT.email}?${q.join('&')}`;
}
