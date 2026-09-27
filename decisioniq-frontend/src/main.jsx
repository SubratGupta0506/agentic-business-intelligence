import React,{useEffect,useState,useMemo} from 'react';
import {createRoot} from 'react-dom/client';
import {
  Database,Brain,Search,FileText,Activity,Workflow,BarChart3,Settings,
  ArrowRight,ArrowUpRight,Terminal,Server,Layers,Sparkles,GitBranch,
  ClipboardList,BookOpen,ShieldCheck,CheckCircle2,PlugZap
} from 'lucide-react';
import './styles.css';

// ---------------------------------------------------------------------------
// Static product data (unchanged from the original build)
// ---------------------------------------------------------------------------
const API='http://127.0.0.1:8000';
const dataset={transactions:'51,290',orders:'25,035',customers:'4,873',products:'10,292',sales:'$12.64M',profit:'$1.47M',period:'2011 — 2014'};
const columns=[
 ['category','Category','Categorical','Product grouping'],['city','City','Categorical','Customer/order geography'],['country','Country','Categorical','Market geography'],['customer_id','Customer ID','Identifier','Customer key'],['customer_name','Customer Name','Identifier','Customer name'],['discount','Discount','Numeric','Recorded discount proportion'],['market','Market','Categorical','Commercial market'],['order_date','Order Date','Date','Transaction date'],['order_id','Order ID','Identifier','Order key'],['order_priority','Order Priority','Categorical','Order priority'],['product_id','Product ID','Identifier','Product key'],['product_name','Product Name','Categorical','Product name'],['profit','Profit','Numeric','Transaction profit'],['quantity','Quantity','Numeric','Units sold'],['region','Region','Categorical','Business region'],['row_id','Row ID','Identifier','Transaction row key'],['sales','Sales','Numeric','Transaction sales'],['segment','Segment','Categorical','Customer segment'],['ship_date','Ship Date','Date','Shipment date'],['ship_mode','Ship Mode','Categorical','Shipping mode'],['shipping_cost','Shipping Cost','Numeric','Shipping cost'],['state','State','Categorical','Customer/order state'],['sub_category','Sub-Category','Categorical','Product sub-category'],['market_2','Market 2','Categorical','Normalized market field'],['profit_margin','Profit Margin','Numeric','Profit relative to sales']
];
const fieldGroups=[
 ['IDENTIFIERS',['row_id','order_id','customer_id','product_id']],
 ['TIME',['order_date','ship_date']],
 ['BUSINESS DIMENSIONS',['region','country','market','category','sub_category','segment','ship_mode','order_priority']],
 ['MEASURES',['sales','profit','quantity','discount','shipping_cost','profit_margin']],
];
const docs=[
 ['company_business_overview.md','Business Overview'],
 ['pricing_discount_policy.md','Pricing & Discount Policy'],
 ['shipping_fulfillment_policy.md','Shipping & Fulfillment Policy'],
 ['customer_segmentation_strategy.md','Customer Segmentation Strategy'],
 ['product_category_management.md','Product Category Management'],
 ['business_kpi_definitions.md','Business KPI Definitions'],
 ['root_cause_analysis_playbook.md','Root Cause Analysis Playbook'],
 ['business_analysis_governance.md','Business Analysis Governance'],
 ['business_scenario_playbook.md','Business Scenario Playbook'],
 ['business_data_dictionary.md','Business Data Dictionary'],
];
const examples=[
 ['REVENUE','Why did sales decline in July 2014 compared with June 2014?'],
 ['PROFITABILITY','Which regions contributed most to the July 2014 profit decline?'],
 ['DISCOUNT','Did discounting increase while profitability declined?'],
 ['REGIONS','Which regions experienced the largest sales reduction?'],
 ['OPERATIONS','What operational metrics changed when sales declined?'],
 ['POLICY','What does the discount policy say about higher discount levels?'],
];
const nav=[
 ['overview','Overview',BarChart3],
 ['dataset','Dataset Explorer',Database],
 ['investigate','Investigation Desk',Brain],
 ['knowledge','Business Knowledge',BookOpen],
 ['architecture','System Architecture',GitBranch],
];
const pageLabel={overview:'OVERVIEW',dataset:'DATASET EXPLORER',investigate:'INVESTIGATION DESK',knowledge:'BUSINESS KNOWLEDGE',architecture:'SYSTEM ARCHITECTURE'};

// ---------------------------------------------------------------------------
// App shell
// ---------------------------------------------------------------------------
function App(){
 const [page,setPage]=useState('overview');
 const [q,setQ]=useState('');
 const [answer,setAnswer]=useState('');
 const [loading,setLoading]=useState(false);
 const [error,setError]=useState('');
 const [health,setHealth]=useState('checking');

 useEffect(()=>{fetch(`${API}/`).then(r=>setHealth(r.ok?'online':'offline')).catch(()=>setHealth('offline'));},[]);

 const ask=async()=>{
  if(!q.trim())return;
  setLoading(true);setError('');setAnswer('');setPage('investigate');
  try{
   const r=await fetch(`${API}/api/ask`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q.trim()})});
   const d=await r.json();
   if(!r.ok)throw new Error(d.detail||d.error||'Investigation failed');
   const out=d.answer||d.response||d.result||d.message||d.output;
   setAnswer(typeof out==='string'?out:JSON.stringify(d,null,2));
  }catch(e){setError(e.message)}
  finally{setLoading(false)}
 };
 const askWith=(text)=>{setQ(text);setPage('investigate')};
 const newCase=()=>{setQ('');setAnswer('');setError('');setPage('investigate')};

 return <div className="app-shell">
  <aside className="sidebar">
   <div className="brand">
    <div className="brandmark"><span>DQ</span></div>
    <div><div className="brand-name">Decision<em>IQ</em></div><span className="brand-sub">Agentic Business Intelligence</span></div>
   </div>
   <div className="nav-section">
    <label className="nav-label">Control Room</label>
    {nav.map(([id,label,Icon])=>
     <button key={id} className={page===id?'nav-item active':'nav-item'} onClick={()=>setPage(id)}>
      <Icon size={16}/><span>{label}</span>
      {id==='investigate'&&<span className="nav-tag">AI</span>}
     </button>
    )}
   </div>
   <div className="status-panel">
    <label className="status-title">System Status</label>
    <div className="status-row"><span className="status-dot"/><b>PostgreSQL Connected</b></div>
    <div className="status-row"><span className="status-dot"/><b>FAISS Connected</b></div>
    <div className="status-row"><span className={health==='online'?'status-dot':'status-dot off'}/><b>FastAPI {health==='online'?'Connected':health==='offline'?'Offline':'Checking…'}</b></div>
   </div>
  </aside>
  <main className="workspace">
   <header className="topbar">
    <div className="crumb"><span>DECISIONIQ</span><b>/</b><strong>{pageLabel[page]}</strong></div>
    <div className="top-actions">
     <div className={health==='online'?'backend-status':'backend-status offline'}>
      <span className="dot"/>{health==='online'?'Backend Online':health==='offline'?'Backend Offline':'Checking Backend'}
     </div>
     <button className="new-investigation-btn" onClick={newCase}><Sparkles size={15}/> New Investigation</button>
    </div>
   </header>
   {page==='overview'&&<Overview setPage={setPage} askWith={askWith}/>}
   {page==='dataset'&&<Dataset/>}
   {page==='investigate'&&<Investigation q={q} setQ={setQ} ask={ask} loading={loading} answer={answer} error={error} askWith={askWith}/>}
   {page==='knowledge'&&<Knowledge/>}
   {page==='architecture'&&<Architecture/>}
  </main>
 </div>;
}

function SectionTitle({eyebrow,title,desc,action}){
 return <div className="section-title">
  <div><span className="eyebrow">{eyebrow}</span><h2>{title}</h2>{desc&&<p>{desc}</p>}</div>
  {action}
 </div>;
}

// ---------------------------------------------------------------------------
// Overview
// ---------------------------------------------------------------------------
function Overview({setPage,askWith}){
 return <div className="page">
  <section className="hero">
   <div>
    <span className="hero-kicker"><Sparkles size={12}/> Agentic Business Intelligence</span>
    <h1>Investigate business decisions with AI.</h1>
    <p>DecisionIQ combines structured analytics, business knowledge retrieval, and LangGraph agent orchestration to turn complex business questions into evidence-backed insights.</p>
    <div className="hero-actions">
     <button className="btn-primary" onClick={()=>setPage('investigate')}>Start Investigation <ArrowRight size={16}/></button>
     <button className="btn-secondary" onClick={()=>setPage('dataset')}>Explore Dataset</button>
    </div>
    <div className="hero-tags">
     <span><i/> LangGraph orchestration</span>
     <span><i/> PostgreSQL analytics</span>
     <span><i/> FAISS / RAG retrieval</span>
    </div>
   </div>
   <div className="hero-diagram">
    <div className="hero-diagram-head"><span>AGENT RUNTIME</span><b>● READY</b></div>
    <div className="hero-node-stack">
     <div className="hero-node"><div className="hn-icon"><ClipboardList size={16}/></div><div><b>Question</b><small>Natural language intent</small></div></div>
     <div className="hero-connector"><i/></div>
     <div className="hero-node core"><div className="hn-icon"><Brain size={16}/></div><div><b>Planner</b><small>LangGraph orchestration</small></div></div>
     <div className="hero-connector"><i/></div>
     <div className="hero-node"><div className="hn-icon"><Database size={16}/></div><div><b>Tools</b><small>PostgreSQL + FAISS/RAG</small></div></div>
     <div className="hero-connector"><i/></div>
     <div className="hero-node"><div className="hn-icon"><CheckCircle2 size={16}/></div><div><b>Insight</b><small>Evidence-backed answer</small></div></div>
    </div>
   </div>
  </section>

  <section className="metric-strip">
   <Metric value={dataset.sales} label="Total Sales"/>
   <Metric value={dataset.profit} label="Total Profit"/>
   <Metric value={dataset.transactions} label="Transactions"/>
   <Metric value={dataset.orders} label="Orders"/>
   <Metric value={dataset.customers} label="Customers"/>
   <Metric value={dataset.products} label="Products"/>
  </section>

  <section className="runtime-grid">
   <div className="panel panel-pad">
    <div className="panel-head"><h3>Agent Execution Pipeline</h3><span className="live-chip"><i/> Ready</span></div>
    <div className="flow-row">
     <div className="flow-step"><small>Question</small><b>User intent</b></div>
     <div className="flow-arrow"><ArrowRight size={16}/></div>
     <div className="flow-step dark"><small>Planner</small><b>LangGraph</b></div>
     <div className="flow-arrow"><ArrowRight size={16}/></div>
     <div className="flow-step"><small>Tools</small><b>SQL + RAG</b></div>
     <div className="flow-arrow"><ArrowRight size={16}/></div>
     <div className="flow-step"><small>Evidence</small><b>Findings</b></div>
     <div className="flow-arrow"><ArrowRight size={16}/></div>
     <div className="flow-step accent"><small>Insight</small><b>Decision</b></div>
    </div>
    <div className="agent-console">
     <div className="agent-console-head"><span className="term-dot green"/><span className="term-dot"/><span className="term-dot"/><b>agent-runtime</b></div>
     <code><span>01</span>ready · awaiting business question</code>
     <code><span>02</span>toolbelt · SQL analytics + semantic retrieval</code>
     <code><span>03</span>context · 51,290 transactions / 10 documents</code>
    </div>
   </div>
   <div className="panel panel-pad">
    <div className="panel-head"><h3>Ask DecisionIQ</h3><span className="live-chip" style={{color:'var(--muted)',background:'transparent',border:'1px solid var(--border)'}}>{examples.length} patterns</span></div>
    <div className="pattern-list">
     {examples.map((x,i)=>
      <button className="pattern-item" key={x[0]} onClick={()=>askWith(x[1])}>
       <span>{String(i+1).padStart(2,'0')}</span>
       <div><small>{x[0]}</small><b>{x[1]}</b></div>
       <em><ArrowUpRight size={14}/></em>
      </button>
     )}
    </div>
   </div>
  </section>

  <SectionTitle eyebrow="System Capabilities" title="Evidence layers, one agentic workspace." desc="The interface exposes the same layers the investigation engine uses to reach a conclusion."/>
  <div className="cap-grid">
   <Capability icon={Database} tag="SQL Tooling" title="Structured analytics" text="PostgreSQL-backed trends, comparisons, dimensions and operational metrics."/>
   <Capability icon={Search} tag="RAG / FAISS" title="Business knowledge" text="Semantic retrieval over policies, KPI definitions, strategy and playbooks."/>
   <Capability icon={Workflow} tag="LangGraph" title="Agent orchestration" text="LangGraph coordinates planning, tool execution and investigation state."/>
   <Capability icon={Server} tag="FastAPI" title="Application API" text="FastAPI provides the local interface between the agent and DecisionIQ."/>
  </div>
 </div>;
}
function Metric({value,label}){return <div className="metric-card"><strong>{value}</strong><span>{label}</span></div>}
function Capability({icon:Icon,tag,title,text}){return <div className="cap-card"><div className="cap-icon"><Icon size={17}/></div><small>{tag}</small><h3>{title}</h3><p>{text}</p></div>}

// ---------------------------------------------------------------------------
// Dataset Explorer
// ---------------------------------------------------------------------------
function Dataset(){
 const [term,setTerm]=useState('');
 const filtered=useMemo(()=>{
  const t=term.trim().toLowerCase();
  if(!t)return columns;
  return columns.filter(c=>c.join(' ').toLowerCase().includes(t));
 },[term]);
 return <div className="page">
  <SectionTitle eyebrow="Data Explorer / Transaction Layer" title="Explore the business dataset." desc="51,290 transactions spanning 2011 – 2014, cleaned into 25 analytical fields and loaded into PostgreSQL." action={<div className="pill-badge"><span className="dot"/> PostgreSQL <b>Connected</b></div>}/>

  <section className="stat-row">
   <div className="stat-card">
    <span>TRANSACTION TABLE</span><strong>51,290</strong>
    <div className="bar-track"><div className="bar-fill" style={{width:'82%'}}/></div>
    <div className="entity-row" style={{marginTop:14}}><div><strong style={{fontSize:13,fontWeight:600,color:'var(--text2)'}}>25 columns</strong></div><div><strong style={{fontSize:13,fontWeight:600,color:'var(--text2)'}}>2011 — 2014</strong></div></div>
   </div>
   <div className="stat-card">
    <span>BUSINESS ENTITIES</span>
    <div className="entity-row">
     <div><strong>25,035</strong><span>Orders</span></div>
     <div><strong>4,873</strong><span>Customers</span></div>
     <div><strong>10,292</strong><span>Products</span></div>
    </div>
   </div>
   <div className="stat-card">
    <span>CORE MEASURES</span>
    <p style={{fontSize:13,color:'var(--text2)',lineHeight:1.7,marginTop:14}}>Sales · Profit · Quantity · Discount · Shipping Cost · Profit Margin</p>
   </div>
  </section>

  <div className="field-groups">
   {fieldGroups.map(([name,fields])=>
    <div className="field-group" key={name}>
     <h4>{name}</h4>
     <ul>{fields.map(f=><li key={f}>{f}</li>)}</ul>
    </div>
   )}
  </div>

  <section className="table-card">
   <div className="table-toolbar">
    <div><span className="eyebrow">Schema Registry</span> <b style={{marginLeft:8}}>25 fields</b></div>
    <div className="search-box"><Search size={14}/><input placeholder="Search transaction schema…" value={term} onChange={e=>setTerm(e.target.value)}/></div>
   </div>
   <div className="table-wrap">
    <table>
     <thead><tr><th>Field</th><th>Display</th><th>Type</th><th>Purpose</th></tr></thead>
     <tbody>{filtered.map(c=><tr key={c[0]}><td><code>{c[0]}</code></td><td>{c[1]}</td><td><span className="type-pill">{c[2]}</span></td><td>{c[3]}</td></tr>)}</tbody>
    </table>
   </div>
  </section>

  <div className="info-grid">
   <InfoCard icon={Layers} title="Dimensions" text="Region · Market · Country · Category · Sub-Category · Segment · Ship Mode"/>
   <InfoCard icon={Activity} title="Time intelligence" text="Order Date and Ship Date support monthly, period and operational comparisons."/>
   <InfoCard icon={ShieldCheck} title="Agent boundary" text="The agent can reason only over connected data and indexed business knowledge."/>
  </div>
 </div>;
}
function InfoCard({icon:Icon,title,text}){return <div className="info-card"><Icon size={17}/><div><b>{title}</b><p>{text}</p></div></div>}

// ---------------------------------------------------------------------------
// Investigation Desk
// ---------------------------------------------------------------------------
function Investigation({q,setQ,ask,loading,answer,error}){
 return <div className="page">
  <SectionTitle eyebrow="Investigation Engine / Case Desk" title="What needs investigating?" desc="Ask a why, what-changed, where, or impact question. The agent can combine structured analytics with business knowledge." action={<div className="pill-badge"><span className="dot"/> Case <b>Local</b></div>}/>

  <div className="investigation-grid">
   <div className="desk-col">
    <div className="question-panel">
     <div className="question-panel-head"><div><Terminal size={14}/> Agent Console</div><span style={{fontSize:11,color:'var(--success)',fontWeight:600}}>Ready</span></div>
     <textarea value={q} onChange={e=>setQ(e.target.value)} placeholder="Ask a business question… e.g. Why did sales decline in July 2014 compared with June 2014?"/>
     <div className="question-panel-foot">
      <span>SQL + RAG toolbelt enabled</span>
      <button className="run-btn" disabled={loading||!q.trim()} onClick={ask}>{loading?'Investigating…':'Run investigation'} {!loading&&<ArrowRight size={15}/>}</button>
     </div>
    </div>
    <div className="example-list">
     <h4>Investigation Patterns</h4>
     {examples.map((x,i)=>
      <button className="example-row" key={x[0]} onClick={()=>setQ(x[1])}>
       <span>{String(i+1).padStart(2,'0')}</span>
       <div><small>{x[0]}</small><b>{x[1]}</b></div>
       <em>+</em>
      </button>
     )}
    </div>
   </div>

   <div className="desk-col">
    <div className="timeline-panel">
     {!loading&&!answer&&!error&&
      <div className="timeline-empty">
       <Brain size={30}/>
       <b>Awaiting a question</b>
       <p>Run an investigation to see the agent assemble evidence and produce a business insight here.</p>
      </div>}
     {loading&&
      <div className="trace-list">
       <div className="trace-step"><div className="trace-dot"><i/></div><div><b>Understanding the question</b><small>Parsing intent and scope</small></div></div>
       <div className="trace-step"><div className="trace-dot"><i/></div><div><b>Selecting analytical tools</b><small>SQL analytics and semantic retrieval</small></div></div>
       <div className="trace-step"><div className="trace-dot"><i/></div><div><b>Collecting evidence</b><small>Structured data and business knowledge</small></div></div>
       <div className="trace-step"><div className="trace-dot"><i/></div><div><b>Synthesizing insight</b><small>Composing the final answer</small></div></div>
      </div>}
     {error&&
      <div className="error-card"><b>Investigation failed</b><p>{error}</p></div>}
     {!loading&&answer&&
      <div className="result-panel">
       <div className="result-head"><h3>Investigation Result</h3><span className="completed-chip"><CheckCircle2 size={13}/> Completed</span></div>
       <div className="result-block conclusion-block">
        <div className="result-block-head"><Sparkles size={13}/> Conclusion</div>
        <div className="result-block-body"><div className="answer-text">{answer}</div></div>
       </div>
      </div>}
    </div>
   </div>

   <div className="desk-col">
    <div className="evidence-panel">
     <h4>Connected Evidence</h4>
     <ToolBadge icon={Database} name="PostgreSQL" text="Structured business analytics"/>
     <ToolBadge icon={Search} name="FAISS / RAG" text="Business knowledge retrieval"/>
     <ToolBadge icon={Workflow} name="LangGraph" text="Agent orchestration"/>
     <ToolBadge icon={PlugZap} name="FastAPI" text="Application interface"/>
    </div>
   </div>
  </div>
 </div>;
}
function ToolBadge({icon:Icon,name,text}){return <div className="tool-badge"><div className="tb-icon"><Icon size={16}/></div><div><b>{name}</b><small>{text}</small></div><CheckCircle2 size={15} className="tb-status"/></div>}

// ---------------------------------------------------------------------------
// Business Knowledge
// ---------------------------------------------------------------------------
function Knowledge(){
 return <div className="page">
  <SectionTitle eyebrow="Knowledge Base / Semantic Layer" title="Business knowledge the agent can retrieve." desc="DecisionIQ retrieves relevant business policies, definitions and playbooks when structured data alone is not enough." action={<div className="pill-badge"><span className="dot"/> FAISS <b>179 chunks</b></div>}/>

  <section className="knowledge-stats">
   <div className="knowledge-stat"><span>VECTOR INDEX</span><strong>179</strong>
    <div className="vector-bars">{Array.from({length:18}).map((_,i)=><i key={i} style={{height:(22+(i%6)*8)+'%'}}/>)}</div>
    <p>Retrievable chunks indexed for semantic search.</p>
   </div>
   <div className="knowledge-stat"><span>EMBEDDINGS</span><strong>384</strong><p>Dimensions per vector, produced by all-MiniLM-L6-v2 and stored in a persistent FAISS IndexFlatIP.</p></div>
   <div className="knowledge-stat"><span>DOCUMENTS</span><strong>10</strong><p>Policies, KPI definitions, governance and root-cause playbooks.</p></div>
  </section>

  <div className="doc-grid">
   {docs.map(([file,name],i)=>
    <div className="doc-card" key={file}>
     <div className="doc-icon"><FileText size={17}/></div>
     <div>
      <span>Markdown · Business Knowledge</span>
      <h3>{name}</h3>
      <p>Indexed document available to semantic retrieval and agent investigations.</p>
      <div className="doc-status"><CheckCircle2 size={12}/> Indexed</div>
     </div>
     <b><ArrowUpRight size={14}/></b>
    </div>
   )}
  </div>
 </div>;
}

// ---------------------------------------------------------------------------
// System Architecture
// ---------------------------------------------------------------------------
function Architecture(){
 return <div className="page">
  <SectionTitle eyebrow="Agent Graph / Orchestration" title="How DecisionIQ thinks through a business question." desc="DecisionIQ is designed as an investigation system, not a chat wrapper: question → planning → tools → evidence → answer." action={<div className="pill-badge"><span className="dot"/> Graph <b>Ready</b></div>}/>

  <div className="arch-diagram">
   <div className="arch-col">
    <div className="arch-node"><div className="an-icon"><ClipboardList size={16}/></div><div><b>User</b><small>Business question</small></div></div>
    <div className="arch-connector"><i/></div>
    <div className="arch-node"><div className="an-icon"><Server size={16}/></div><div><b>FastAPI</b><small>/api/ask</small></div><div className="an-status"><i/>Connected</div></div>
    <div className="arch-connector"><i/></div>
    <div className="arch-node main"><div className="an-icon"><Brain size={16}/></div><div><b>LangGraph Agent</b><small>Planning + tool execution</small></div><div className="an-status"><i/>Ready</div></div>
    <div className="arch-branch-wrap">
     <div className="arch-branch">
      <div className="arch-node"><div className="an-icon"><Database size={16}/></div><div><b>PostgreSQL</b><small>51,290 transactions</small></div><div className="an-status"><i/>Connected</div></div>
      <div className="arch-node"><div className="an-icon"><Search size={16}/></div><div><b>FAISS + RAG</b><small>179 vectors</small></div><div className="an-status"><i/>Connected</div></div>
     </div>
    </div>
    <div className="arch-connector"><i/></div>
    <div className="arch-node"><div className="an-icon"><ClipboardList size={16}/></div><div><b>Evidence</b><small>Metrics + documents</small></div></div>
    <div className="arch-connector"><i/></div>
    <div className="arch-node main"><div className="an-icon"><CheckCircle2 size={16}/></div><div><b>Business Insight</b><small>Evidence-backed answer</small></div></div>
   </div>
  </div>

  <div className="layer-grid">
   <Layer n="01" title="Data layer" text="51,290 transaction rows in PostgreSQL provide deterministic business analytics."/>
   <Layer n="02" title="Knowledge layer" text="10 documents become 179 chunks with 384-dimensional semantic embeddings."/>
   <Layer n="03" title="Agent layer" text="LangGraph coordinates state, tool selection and investigation flow."/>
   <Layer n="04" title="Application layer" text="FastAPI exposes the local agent to the DecisionIQ interface."/>
  </div>
 </div>;
}
function Layer({n,title,text}){return <div className="layer-card"><span className="layer-num">{n}</span><h3>{title}</h3><p>{text}</p></div>}

createRoot(document.getElementById('root')).render(<App/>);
