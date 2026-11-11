"use strict";
// This website is a GitHub-linked guide, not the scam detection backend.
// Do not store user messages, passwords, secrets, or GitHub tokens here.
const REPO = 'HinkChao/ScamShield';
const team = [
  { initials:'AA',name:'Athar Alimmudin',role:'Product · Research · Integration',detail:'Align product goals, module contracts, research evidence, and end-to-end integration.',issues:[9,13]},
  { initials:'JM',name:'Josue Martinez-Martinez',role:'Machine Learning · AI Engineering',detail:'Build a reproducible text classifier with inference, tests, and documented data provenance.',issues:[6]},
  { initials:'AI',name:'Anna Ishimatsu',role:'UX · Outreach · Responsible AI',detail:'Create accessible, multilingual risk explanations and help shape the responsible-AI narrative.',issues:[11,13]},
  { initials:'AT',name:'Atho',role:'Cybersecurity · URL Engineering',detail:'Develop safe, static URL parsing and suspicious-link test cases.',issues:[7]},
  { initials:'HC',name:'Hink',role:'Application · UI Development',detail:'Connect the existing Streamlit interface to tested backend components.',issues:[8]},
  { initials:'SA',name:'Samantha',role:'Evaluation · Testing · QA',detail:'Validate the pipeline, report failure cases, and extend the existing evaluation work.',issues:[10]}
];
const tasks = [
  {n:6,title:'ML phishing classifier',desc:'Training, inference, reproducible model evaluation'},
  {n:7,title:'Static URL security',desc:'Safe parsing, deceptive link detection, tests'},
  {n:8,title:'Streamlit application',desc:'User input, backend integration, results UI'},
  {n:9,title:'Risk assessment & explanations',desc:'Evidence contracts, uncertainty, safe guidance'},
  {n:10,title:'Evaluation & QA',desc:'Dataset protocol, metrics, test suite'},
  {n:11,title:'Multilingual UX',desc:'English and Traditional Chinese, accessibility'},
  {n:12,title:'QR decoding (optional)',desc:'Stretch goal only after the core app works'},
  {n:13,title:'Pitch & adoption',desc:'Showcase, limitations, contributions, responsible outreach'}
];
const issueLink = n=>`https://github.com/${REPO}/issues/${n}`;
const escapeHtml = s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function renderTeam(){document.querySelector('#teamCards').innerHTML=team.map(m=>`<article class="card"><div class="avatar" aria-hidden="true">${m.initials}</div><h3>${escapeHtml(m.name)}</h3><div class="role">${escapeHtml(m.role)}</div><p>${escapeHtml(m.detail)}</p><p class="deliverable">Proposed work: ${m.issues.map(n=>`<a href="${issueLink(n)}" target="_blank" rel="noopener noreferrer">#${n} ↗</a>`).join(' · ')}</p></article>`).join('');}
function renderIssues(live){document.querySelector('#issues').innerHTML=tasks.map(t=>{const issue=live?.get(t.n);const state=issue?.state;const assignees=issue?.assignees?.map(a=>a.login).join(', ');return `<div class="issue"><div><strong>#${t.n} · ${escapeHtml(t.title)}</strong><small>${escapeHtml(t.desc)}</small></div><div class="meta">${state?`<span class="status">${escapeHtml(state)}${assignees?' · @'+escapeHtml(assignees):' · unassigned'}</span>`:''}<a href="${issueLink(t.n)}" target="_blank" rel="noopener noreferrer">Open Issue ↗</a></div></div>`;}).join('');}
async function refreshIssues(){const status=document.querySelector('#issueStatus');try{const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),5000);let response;try{response=await fetch(`https://api.github.com/repos/${REPO}/issues?state=all&per_page=100`,{signal:controller.signal,headers:{Accept:'application/vnd.github+json'}});}finally{clearTimeout(timeout)}if(!response.ok)throw Error('GitHub status unavailable');const all=await response.json();const live=new Map(all.filter(x=>!x.pull_request).map(x=>[x.number,x]));renderIssues(live);status.textContent='Live issue status from GitHub';}catch(e){status.textContent='Live status unavailable · Use GitHub links for current details';}}
renderTeam();renderIssues();refreshIssues();
