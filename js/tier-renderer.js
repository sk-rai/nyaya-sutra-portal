// Tier Renderer - Dynamically renders case cards based on user tier

const CASE_DATA = [
  {
    id: 1,
    number: "AFT/DEL/2023/1234",
    date: "15 Feb 2026",
    title: "Rajesh Kumar vs. Union of India",
    bench: "Justice A. Sharma",
    type: "Service Matter",
    status: "For Hearing",
    counsel: "Adv. S. Patel",
    venue: "Court Room No. 5"
  },
  {
    id: 2,
    number: "CGAT/DEL/2024/5678",
    date: "18 Feb 2026",
    title: "Suresh Patel vs. Ministry of Defence",
    bench: "Justice B. Mehta",
    type: "Pension Dispute",
    status: "Disposed",
    counsel: "Adv. R. Singh",
    venue: "Court Room No. 3"
  },
  {
    id: 3,
    number: "AFT/DEL/2023/9012",
    date: "20 Feb 2026",
    title: "Meena Devi vs. Indian Army",
    bench: "Justice C. Reddy",
    type: "Service Matter",
    status: "For Hearing",
    counsel: "Adv. P. Kumar",
    venue: "Court Room No. 7"
  }
];

// Show upgrade modal
function showUpgradeModal() {
  alert('Please upgrade your plan to access full case details, counsel names, and venue information.');
}

// Print case
function printCase(caseId) {
  const caseItem = CASE_DATA.find(c => c.id === caseId);
  if (caseItem) {
    window.print();
  }
}

// Copy case
function copyCase(caseId) {
  const caseItem = CASE_DATA.find(c => c.id === caseId);
  if (caseItem) {
    const text = `${caseItem.number} - ${caseItem.title}\nDate: ${caseItem.date}\nBench: ${caseItem.bench}\nVenue: ${caseItem.venue}`;
    navigator.clipboard.writeText(text).then(() => {
      alert('Case details copied to clipboard!');
    });
  }
}