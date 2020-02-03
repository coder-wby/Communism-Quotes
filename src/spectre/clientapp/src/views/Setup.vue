<template>
    <v-container>

        <v-row>
            <h1 class="text-left">run setup here</h1>
        </v-row>

        <v-row>
            <v-col cols="6">
                <v-slider min="0" max="100" v-model="x"/>
                <v-text-field label="js values" readonly v-model="x"/>
                <v-btn @click="onBtnClick1">运行</v-btn>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="5">
                <v-text-field label="input something 1" v-model="keyword1" filled required/>
                <v-text-field label="input something 2" v-model="keyword2" filled/>
                <v-btn @click="onBtnClick2">call query service</v-btn>
                <v-textarea v-model="result"/>
            </v-col>
        </v-row>

    </v-container>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import axios from 'axios';

    @Component
    export default class Home extends Vue {
        private x: number = 0;
        private keyword1: string = "无产阶级";
        private keyword2: string = "组织";
        private result: string = "";

        onBtnClick1(): void {
            this.x += 1;
        }

        onBtnClick2(): void {
            axios.get(`http://localhost:5000/query/${this.keyword1}%20${this.keyword2}`)
                .then(response => (this.result = response.data.toString()))
        }
    }
</script>