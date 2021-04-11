import React from 'react';
import ReactDOM from 'react-dom';
import { Container, Button, Table } from 'react-bootstrap/'
import './index.css';

const n = 5;
const m = 10;

class Square extends React.Component {
    render() {
        return (
            <td>
                <Button variant="success" className="square">
                </Button>
            </td>
        );
    }
}

class Board extends React.Component {
    renderSquare(i) {
        return <Square />;
    }

    createSquares() {
        const squares = [];
        for (var columnIndex = 0; columnIndex < m; columnIndex++) {
            squares.push(this.renderSquare(columnIndex));
        }
        return squares
    }

    createBoard() {
        const rows = [];
        for (var rowIndex = 0; rowIndex < n; rowIndex++) {
            rows.push(
                <div className="board-row">
                    <tr>
                        {this.createSquares()}
                    </tr>
                </div>);
        }
        return rows;
    }

    render() {
        const status = 'Forest fire';

        return (
            <div>
                <div className="status">{status}</div>
                <Table>
                    <tbody>
                        {this.createBoard()}
                    </tbody>
                </Table>
            </div>
        );
    }
}

class Game extends React.Component {
    render() {
        return (
            <div className="game">
                <div className="game-board">
                    <Board />
                </div>
                <div className="game-info">
                    <div>{/* status */}</div>
                    <ol>{/* TODO */}</ol>
                </div>
            </div>
        );
    }
}

// ========================================

ReactDOM.render(
    <Game />,
    document.getElementById('root')
);
