import React from 'react';


class PollResult extends React.Component{
    
    state = {
        pollId: this.props.match.params.id,
        pollData: {},
    }

    constructor(props){
        super(props);
        
    }

    componentDidMount(){
        const resultUrl = `/api/poll/${this.state.pollId}/result/`
        fetch(resultUrl)
            .then(response => {
                if (response.status !== 200) {
                    throw Error(`The status in fetching poll result id ${response.status}`)
                }
                return response.json();
            })    
            .then(result => {
                this.setState({pollData: result})
            })
    }

    render(){
        return !this.state.pollData ? 
        'Результаты опроса не готовы' :
         (
            <div id="poll-result">
                <h2>
                    {this.state.pollData.name }
                </h2>
                <div className="description">
                    Ваш результат: {this.state.pollData.score} / {this.state.pollData.maxScorePossible}
                </div>
            </div>
        )
    }
}

export default PollResult;