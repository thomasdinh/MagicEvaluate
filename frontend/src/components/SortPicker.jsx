import "../css/sort-picker.css"

function SortPicker({ onChange }){
    return (
        <label className="sortLabel">
          Sort Order:  
          <select name="sortOrder" className="sort-picker" onChange={onChange}>
            <option value="name_asc">Name Asc.  (A-Z)</option>
            <option value="name_desc">Name Desc. (Z-A)</option>
            <option value="asc_winrate">Winrate Asc. (0-100)</option>
            <option value="desc_winrate">Winrate Desc. (100-0)</option>
          </select>
        </label>
      );
}

export default SortPicker;