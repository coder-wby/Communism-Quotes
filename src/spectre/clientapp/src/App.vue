<template>
    <v-app>
        <v-app-bar app color="primary" dark>
            <h2>导师们的话</h2>
            <v-spacer/>
            <v-btn text to="/">Home</v-btn>
            <v-btn text to="/setup">Setup</v-btn>
            <v-btn text to="/about">About</v-btn>
        </v-app-bar>
        <v-content>
            <router-view/>
        </v-content>
    </v-app>
</template>

<style> * {
    /* button不要全部大写 */
    text-transform: none !important;
} </style>
