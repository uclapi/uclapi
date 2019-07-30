import Column from '../containers/Column.jsx';

class ColumnNode {
  
  constructor() {
    this.children = [];
  }

  add(children) {
    children.forEach(function(child) {
      this.children.push(child);
    });
  }

  getView() {
    return <Column>
    			{this.children.map((child) => child.getView())}
		   </Column>
  }
  
}