import React from 'react';
import ApiService from '../ApiService';

const Homepage = () => {
  const [customer, setCustomer] = React.useState(["I want to order chinese food but I can't speak Chinese.", "I would like fried rice."]);
  const [waiter, setWaiter] = React.useState(["我听不懂他在说什么。"])
  const [translations, setTranslations] = React.useState([]);
  const [text, setText] = React.useState("");
  const [isCustomer, setIsCustomer] = React.useState(true);

  const handleUserInput = (e) => {
    setText(e.target.value);

  }

  const HandleSubmit = (e) => {
    // call api
    async function callTranslator() {
        setTranslations([...translations, text]);
        const language = isCustomer ? "CH" : "EN";
        const result = await ApiService.getTranslation(text, language);
        console.log("result: ", result);
        console.log("translation: ", result['text']);
        isCustomer ? setWaiter([...waiter, result['text']]) : setCustomer([...customer, result['text']]);
    }
    e.preventDefault();
    callTranslator();
    setText("");
    setIsCustomer(!isCustomer);
  }

  return (
    <div>
        <div>
            {customer.map((e, i) => <div key={i} className="full-w bg-yellow-300">
                {e}</div>)}
        </div>
        <div>
            {waiter.map((e, i) => <div key={i} className="full-w bg-red-600">
                {e}</div>)}
        </div>
        <div className='full-w'>
            Can you help us?
        </div>
        <form onSubmit={HandleSubmit}>
            <div>{isCustomer ? 'Help Waiter to understand Customer' : 'Help Customer to understand Waiter'}</div>
            <input id="text" type="text" value={text} onChange={handleUserInput} name="text"/>
            <button onClick={HandleSubmit}>Enter!</button>
        </form>
        <h1>Translation(s)</h1>
        <div>
            {translations.map((e, i) => <div key={i} className="bg-green-300">{e}</div>)}
        </div>

    </div>
  )
}

export default Homepage;