import React from 'react';
import { Link } from 'react-router-dom';

class PollControl extends React.Component{
    
    state = {
        pollList: [],
        questionList: [],
    };

    constructor(props){
        super(props);
        this.handleInput = this.handleInput.bind(this);
    }
    
    componentDidMount(){
        this.updatePollList();
    }


    /**
     * Обновить pollList 
     */
    updatePollList(){
        let url = `/api/poll`;
        fetch(url)
            .then(response => {
                if (response.status !== 200 ){
                    throw Error(`The status = ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error(error);
            })
            .then(result => {
                this.setState({pollList: result});
            })
    }

    handleInput(event){
        const name = event.target.getattr('name');
        let stateMap = {};
        stateMap[name] = event.target.value;
        this.setState(stateMap);
    }
    
    
    render(){
        console.log(JSON.stringify(this.state));
        return (
            <div className='control'>
                <div className='poll-control'>
                    <div id='poll-list'>
                        {
                            this.state.pollList.map(poll => {
                                return (
                                    <div className='poll-item'>
                                        {poll.name}
                                        <Link to={`/poll-go/${poll.id}`}>
                                            Начать прохождение
                                        </Link>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
        )
    }
}

export default PollControl;