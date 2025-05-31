<template>
    <div id="user">
        <div class="user-info">
            <h1>Имя пользователя: Иван Иванов Иванович</h1>
            <h1>Email: example@mail.com</h1>
        </div>
        <table>
            <th></th>
            <th>май</th>
            <th>май</th>
            <th>май</th>
            <tr>
                <td>Команда 1</td>
            </tr>
            <tr>
                <td>Команда 2</td>
            </tr>
            <tr>
                <td>Команда 3</td>
            </tr>
        </table>
        <button>Выйти</button>
    </div>
</template>

<script>
export default {
    name: "user",
};
</script>

<style scoped>
.user-info {
    margin: 40px auto;
    display: flex;
    text-align: left;
    flex-direction: column;
    background: #42464e;
    width: 80%;
    border-radius: 20px;
    padding: 20px;
    color: white;
}
button {
    display: block;
    align-self: start;
    margin: 40px auto 0 auto;
    width: 30%;
    height: 5.625rem;
    background: #548dff;
    color: white;
    border: none;
    border-radius: 50px;
    font-size: 25px;
    transition: transform 0.5s ease;
    padding: 20px;
    margin-top: 6.25rem;
}
button:hover {
    background: #497bdf;
    cursor: pointer;
    transform: scale(1.1);
}
table {
    color: white;
}
</style>
