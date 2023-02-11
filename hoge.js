
// 生成したURL
const url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1050436635711957152';

// 書き出し
const updateText = (data) => {
    for (let i = 0; i < data.length; i++) {
        const insertHtml = `
            <li>
                <a href="${data[i].recipeUrl}" target="_blank">
                    <img src="${data[i].foodImageUrl}" alt="${data[i].recipeTitle} 画像">
                </a>
                <h2>${data[i].recipeTitle}</h2>
                <p>${data[i].recipeDescription}</p>
            </li>
        `;
        $('#recipe_list').append(insertHtml);
    }
}

// API取得
$.getJSON(url, (data) => {
    const recipes = data.result;
    updateText(recipes);
});